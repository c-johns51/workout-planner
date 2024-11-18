from django.core.paginator import Paginator
from django.shortcuts import render
import json
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from workoutApp.models import Routine, Exercise, Day
from workoutApp.forms import AddExerciseForm
from ast import literal_eval

# Create your views here.
def home(request):
    return render(request, 'workoutApp/home.html')

def exerciseList(request):

    json_path = Path("../../workout-planner/dist/exercises.json")
    with open(json_path) as json_file:
        data = json.load(json_file)

    paginator = Paginator(data, 20)

    pageNum = request.GET.get('page', 1)

    pageObj = paginator.get_page(pageNum)

    return render(request, 'workoutApp/exerciseList.html', {'pageObj': pageObj})


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
            return redirect('exerciseList')
        else:
            print("Form errors:", form.errors)  # Debugging
    else:
        # Prepopulate form with query parameters
        images = request.GET.get('images', '')
        try:
            images = literal_eval(images) if images else []
        except (ValueError, SyntaxError):
            images = []

        initial_data = {
            'name': request.GET.get('exercise_name', ''),
            'primary_muscles': request.GET.get('primaryMuscles', ''),
            'description': request.GET.get('instructions', ''),
            'images': images,
        }
        form = AddExerciseForm(initial=initial_data)

    return render(request, 'workoutApp/add_to_routine.html', {'form': form})
    
@login_required
def view_routine(request):
    routine = Routine.objects.filter(user=request.user).first()
    days = Day.objects.all()

    # Group exercises by day
    exercises_by_day = {
        day.name: routine.exercises.filter(days=day) if routine else []
        for day in days
    }

    return render(request, 'workoutApp/view_routine.html', {
        'exercises_by_day': exercises_by_day
    })

def remove_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id, routine__user=request.user)
    exercise.delete()
    return redirect('view_routine')