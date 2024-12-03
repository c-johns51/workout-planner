import re
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from workoutApp.models import Routine, Exercise, Day
from workoutApp.forms import AddExerciseForm
from ast import literal_eval
import ast

# Create your views here.
def home(request):
    return render(request, 'workoutApp/home.html')

def exerciseList(request):

    json_path = Path("../../workout-planner/dist/exercises.json")
    with open(json_path) as json_file:
        data = json.load(json_file)

    uniqueMuscles = set()
    for item in data:
        for muscle in item.get('primaryMuscles'):
            uniqueMuscles.add(muscle)

    uniqueMuscles = sorted(uniqueMuscles)

    exerciseQuery = request.GET.get('q', '')
    muscleQuery = request.GET.get('m', '')

    if exerciseQuery:
        regex = re.compile(rf'\b{re.escape(exerciseQuery)}\b', re.IGNORECASE)
        data = [item for item in data if regex.search(item['name'])]

    if muscleQuery:
        data = [item for item in data if muscle in item.get('primaryMuscles')]

    paginator = Paginator(data, 20)

    pageNum = request.GET.get('page', 1)

    pageObj = paginator.get_page(pageNum)

    return render(request, 'workoutApp/exerciseList.html', {'pageObj': pageObj, 'exerciseQuery': exerciseQuery, 'muscleQuery': muscleQuery, 'uniqueMuscles': uniqueMuscles})


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
            return redirect('view_routine')
    else:
        # Prepopulate form with query parameters
        images = request.GET.get('images', '')
        try:
            images = literal_eval(images) if images else []
            if not isinstance(images, list):
                images = []
        except (ValueError, SyntaxError):
            images = []

        initial_data = {
            'name': request.GET.get('exercise_name', ''),
            'primary_muscles': request.GET.get('primaryMuscles', ''),
            'secondary_muscles': request.GET.get('secondaryMuscles', ''),  # Placeholder for future use
            'description': request.GET.get('instructions', ''),
            'images': images,
        }
        form = AddExerciseForm(initial=initial_data)

    return render(request, 'workoutApp/add_to_routine.html', {'form': form})
    
@login_required
def view_routine(request):
    routine = Routine.objects.filter(user=request.user).first()
    days = Day.objects.all()

    # Group exercises by day (default to an empty QuerySet if no routine exists)
    exercises_by_day = {
        day.name: routine.exercises.filter(days=day) if routine else Exercise.objects.none()
        for day in days
    }

    return render(request, 'workoutApp/view_routine.html', {
        'exercises_by_day': exercises_by_day,
        'days': days,
        'routine': routine,
    })

def remove_exercise(request, exercise_id, day):
    """Removes the association of an exercise to a specific day. If deleting the last instance 
    of the exercise in a routine, the exercise is deleted entirely from the routine."""
    exercise = get_object_or_404(Exercise, id=exercise_id, routine__user=request.user)
    day_instance = get_object_or_404(Day, name=day)
    
    # Remove the association between the exercise and the specified day
    exercise.days.remove(day_instance)
    
    # Check if the exercise is still associated with any days
    if not exercise.days.exists():
        exercise.delete()

    return redirect('view_routine')

def exercise_detail(request, exercise_id):
    """
    View to display details of a specific exercise.
    """
    exercise = get_object_or_404(Exercise, id=exercise_id)

    # Convert primary_muscles and secondary_muscles into lists
    primary_muscles = exercise.primary_muscles.strip("[]").replace("'", "").split(", ")
    secondary_muscles = []
    if exercise.secondary_muscles:
        secondary_muscles = exercise.secondary_muscles.strip("[]").replace("'", "").split(", ")
    
    # Initialize the description_sentences list
    description_steps = []

    if exercise.description:
        try:
            description_steps = ast.literal_eval(exercise.description)
        except (ValueError, SyntaxError):
            # If parsing fails, fallback to splitting by '. '
            description_steps = exercise.description.split('. ')
    else:
        description_steps = []
        
    return render(
        request,
        'workoutApp/exercise_detail.html',
        {
            'exercise': exercise,
            'primary_muscles': primary_muscles,
            'secondary_muscles': secondary_muscles,
            'description_steps': description_steps,
        },
    )