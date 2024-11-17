from django.core.paginator import Paginator
from django.shortcuts import render
import json
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from workoutApp.models import Routine, Exercise
from workoutApp.forms import AddExerciseForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def exerciseList(request):

    json_path = Path("../../workout-planner/dist/exercises.json")
    with open(json_path) as json_file:
        data = json.load(json_file)

    paginator = Paginator(data, 20)

    pageNum = request.GET.get('page', 1)

    pageObj = paginator.get_page(pageNum)

    return render(request, 'exerciseList.html', {'pageObj': pageObj})


@login_required
def add_to_routine(request):
    if request.method == "POST":
        form = AddExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            routine, _ = Routine.objects.get_or_create(user=request.user, name="My Routine")
            exercise.routine = routine
            exercise.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('exercise_list')
    else:
        # Prepopulate form with query parameters
        initial_data = {
            'name': request.GET.get('exercise_name', ''),
            'primary_muscles': request.GET.get('primaryMuscles', ''),
            'description': request.GET.get('instructions', ''),
            'images': request.GET.get('images', ''),
        }
        form = AddExerciseForm(initial=initial_data)

    return render(request, 'add_to_routine.html', {'form': form})
    
@login_required
def view_routine(request):
    routine = Routine.objects.filter(user=request.user).first()
    exercises = routine.exercises.all() if routine else []

    return render(request, 'view_routine.html', {'routine': routine, 'exercises': exercises})