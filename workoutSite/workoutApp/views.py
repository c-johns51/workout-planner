from django.shortcuts import render
import json
from pathlib import Path

# Create your views here.
def home(request):
    return render(request, 'home.html')

def exerciseList(request):

    json_path = Path("../../workout-planner/dist/exercises.json")
    with open(json_path) as json_file:
        data = json.load(json_file)

    return render(request, 'exerciseList.html', {'data': data})