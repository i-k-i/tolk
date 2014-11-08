from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from projector.models import Project, Task
from forms import ProjectForm, TaskForm, TaskCommentForm, ProjectCommentForm, MessageForm
from django.contrib import auth
from django.utils import timezone
#from .forms import MessageForm


def projects(request):
    '''Show all project'''
    args = {}
    args.update(csrf(request))
    args['projects'] = Project.objects.all()
    args['username'] = auth.get_user(request).username
    return render_to_response('projects.html', args)

def create_project(request):
    if request.POST:
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.save()
            return HttpResponseRedirect('/projector/all')
    else:
        form = ProjectForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
#    import pdb; pdb.set_trace()
    return render_to_response('create_project.html',args)

def project(request, project_id):
    args = {}
    args['username'] = auth.get_user(request).username
    args['project'] = Project.objects.get(id=project_id)
    args['tasks'] = Task.objects.filter(project__id=project_id).exclude(status='Finished') #only active tasks
#    import pdb ; pdb.set_trace()

    return render_to_response('project.html',args)

def create_task(request, project_id ):
    pr = Project.objects.get(id=project_id)
    if request.POST:
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.creator = request.user
            c.project = pr
            c.save()
            form.save_m2m()
            return HttpResponseRedirect('/projector/project/{}'.format(project_id))
    else:
        form = TaskForm()
    args = {}
    args.update(csrf(request))
    args['project'] = pr
    args['form'] = form
#    import pdb; pdb.set_trace()
    return render_to_response('create_task.html',args)

def create_subtask(request, task_id):
    parent = Task.objects.get(id=task_id)
    pr = Project.objects.get(id=parent.project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.creator = auth.get_user(request)
            c.project = pr
            c.parent_task = parent
            c.save()
            form.save_m2m()
            return HttpResponseRedirect('/projector/project/{}'.format(parent.project_id))
    else:
        form = TaskForm()
    args = {}
    args.update(csrf(request))
    args['project'] = pr
    args['form'] = form
    args['parent'] = parent
#    import pdb; pdb.set_trace()

    return render_to_response('create_task.html',args)

def task_show(request, task_id):
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=task.project.id)
    user = auth.get_user(request)
    real_time = 'not specified'
    if task.status == 'Finished':
        start_date = task.start_date
        if not task.start_date:
            start_date = task.start_date
        real_time = ((task.finish_date - start_date).total_seconds())/60/60
    args = {}
    args['project'] = project
    args['task'] = task
    args['username'] = user.username
    args['real_time'] = real_time
    if user in list(task.workers.all()):
        args['my_task']=True
    if user == task.creator:
        args['creator']=True
    return render_to_response('task.html',args)

def task_accept(request, task_id):
    user = auth.get_user(request)
    task = Task.objects.get(id=task_id)
    task.workers.add(user)
    task.status = 'In work'
    if not task.start_date: # rewrite protection
        task.start_date = timezone.now()
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def task_stop(request, task_id):
    user = auth.get_user(request)
    task = Task.objects.get(id=task_id)
    task.workers.remove(user)
    task.save()
    if task.workers.count()==0:
        task.status = 'Freezed'
        task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def task_done(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'Now check'
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def task_return(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'Returned for revision'
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def task_finish(request, task_id):
#    user = auth.get_user(request)
    task = Task.objects.get(id=task_id)
    now = timezone.now()
#    tdelta = now - task.create_date
    task.status = 'Finished'
    task.finish_date = now
    task.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def all_tasks(reques):
    tasks = Task.objects.all()
#    import pdb; pdb.set_trace()
    args={}
    args['tasks'] = tasks
    args['username'] = auth.get_user(reques).username
    return render_to_response('all_tasks.html', args)

def my_tasks(request):
    user = auth.get_user(request)
    my_tasks = Task.objects.filter(workers__id=user.id).exclude(status='Finished')
    args={}
    args['tasks']=my_tasks
    args['username'] = user.username
    return render_to_response('my_tasks.html',args)

def my_projects(request):
    user = auth.get_user(request)
    #P. S: Mom and Dad this is Chasey
    my_tasks = Task.objects.filter(workers__id=user.id)
    my_projects = Project.objects.filter(task__workers__id=user.id).distinct()

    args={}
    args['my_projects']=my_projects
    args['username'] = user.username

    return render_to_response('my_projects.html',args)

def tests_page(request):
    user = auth.get_user(request)
    form = MessageForm()
    args={}
    args['my_projects'] = my_projects
    args['username'] = user.username
    args['form'] = form
#    return render(request, 'tests_page.html', {'form': form})
    return render_to_response('tests_page.html',args)

def task_comment(request, task_id):
    task = Task.objects.get(id=task_id)
    user = auth.get_user(request)
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.task = task
            c.author = user
            c.save()
#            print form.file
#            import pdb; pdb.set_trace()
            return HttpResponseRedirect('/projector/task/{}'.format(task_id))
    else:
        form = TaskCommentForm()
    args = {}
    args.update(csrf(request))
    args['task'] = task
    args['form'] = form
    args['username'] = user.username
    return render_to_response('task_comment.html',args)

def project_comment(request, project_id):
    project = Project.objects.get(id=project_id)
    user = auth.get_user(request)
    if request.method == 'POST':
        form = ProjectCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.project = project
            c.author = user
            c.save()
            return HttpResponseRedirect('/projector/project/{}'.format(project_id))
    else:
        form = ProjectCommentForm()
    args = {}
    args.update(csrf(request))
    args['project'] = project
    args['form'] = form
    args['username'] = user.username
    return render_to_response('project_comment.html',args)

def welcome(request):
    if '57' in request.COOKIES:
        return HttpResponseRedirect('/projector/all/')
    else:
        response = render_to_response('welcome.html')
        response.set_cookie('57')
        return response

def task_edit(request, task_id ):
    task = Task.objects.get(id=task_id)
    if request.POST:
        form = TaskForm(request.POST, request.FILES, instance = task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projector/task/{}'.format(task_id))
    else:
        form = TaskForm(instance = task)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['task'] = task
    return render_to_response('task_edit.html',args)
