from django import forms
#from docutils.nodes import description
from models import Achievement, AchievementState, QuantityAchievements

class CreateAchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ('name', 'description', 'image')

class NewAchievementFrom(forms.ModelForm):
    class Meta:
        model = AchievementState
        fields = ('user', 'achievement')

class CreateAchievementKitForm(forms.ModelForm):
    class Meta:
        pass
