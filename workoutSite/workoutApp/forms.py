from django import forms
from workoutApp.models import Exercise, Day

class AddExerciseForm(forms.ModelForm):
    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Days of the Week"
    )

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'primary_muscles', 'images', 'days']