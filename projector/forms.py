from django import forms
from models import Project, Task, ProjectComment, TaskComment
from django.contrib.auth.models import User

from django.contrib.admin import widgets

# from nicedit.widgets import NicEditWidget


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'deadline', 'public')

class TaskForm(forms.ModelForm):
    #workers = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    #expected_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    #expected_time = forms.TimeField(widget=widgets.AdminTimeWidget)
    class Meta:
        model = Task
        #fields = ('name', 'expected_time', 'location','description')
        fields = ('name', 'expected_time', 'location','description', 'tags')

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('comment',)

class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ('comment', )

# class MessageForm(forms.Form):
#     message = forms.CharField(
#             widget=NicEditWidget(attrs={'style': 'width: 800px;'}))

#class TaskDoneForm(forms.Form):
#    digress = forms.IntegerField()

class TaskDoneForm(forms.Form):
    digress = forms.IntegerField()


