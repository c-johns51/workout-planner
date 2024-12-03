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
        fields = ['name', 'description', 'primary_muscles', 'secondary_muscles', 'images', 'days']
        widgets = {
            'primary_muscles': forms.HiddenInput(),  # Hide primary muscles
            'secondary_muscles': forms.HiddenInput(),  # Hide secondary muscles
            'description': forms.HiddenInput(),  # Hide description
            'images': forms.HiddenInput(),  # Hide images
        }

    # Clean and validate the images field (if needed)
    def clean_images(self):
        images = self.cleaned_data.get('images')
        if not isinstance(images, list):
            raise forms.ValidationError("Invalid format for images. It should be a list.")
        return images
