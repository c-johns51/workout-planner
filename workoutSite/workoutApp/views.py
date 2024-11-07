from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def exerciseList(request):
    return render(request, 'exerciseList.html')