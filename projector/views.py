from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, Http404
from projector.models import Project, Task, TaskComment, ProjectComment, ProjectorLog
from forms import ProjectForm, TaskForm, TaskCommentForm, ProjectCommentForm, MessageForm, TaskDoneForm
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def loger(user, message, object_name, task=None, project=None):
    event = ProjectorLog(user=user,task=task, project=project, message=message, object_name=object_name)
    event.save()

def task_status_change(task_id, status, user):
    # Stand High Patrol - boat people
    c = TaskComment(author=user, task_id=task_id, comment=status)
    c.save()

def project_status_change(project_id, status, user):
    c = ProjectComment(author=user, project_id=project_id, comment=status)
    c.save()

@login_required(login_url='/auth/login/')
def projects(request):
    '''Show all project'''
    args = {}
    args.update(csrf(request))
    args['projects'] = Project.objects.all()
    args['username'] = auth.get_user(request).username
    loger(auth.get_user(request), 'see all projects', 'all_project')
    return render_to_response('projects.html', args)

@login_required(login_url='/auth/login/')
def create_project(request):
    if request.POST:
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.save()
#            import pdb; pdb.set_trace()
            project = Project.objects.get(id=c.id)
            loger(auth.get_user(request), 'created project',c.name, project=project)
            return HttpResponseRedirect('/projector/all')
    else:
        form = ProjectForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
#    import pdb; pdb.set_trace()
    return render_to_response('create_project.html',args)

@login_required(login_url='/auth/login/')
def project(request, project_id):
    project = Project.objects.get(id=project_id)
    args = {}
    args['username'] = auth.get_user(request).username
    args['project'] = project
    args['tasks'] = Task.objects.filter(project__id=project_id).exclude(status='Finished') #only active tasks
#    import pdb ; pdb.set_trace()
    loger(auth.get_user(request), 'see project', project.name, project=project)

    return render_to_response('project.html',args)

@login_required(login_url='/auth/login/')
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
            loger(auth.get_user(request), 'task_created', c.name, c, pr)
            return HttpResponseRedirect('/projector/project/{}'.format(project_id))
    else:
        form = TaskForm()
    args = {}
    args.update(csrf(request))
    args['project'] = pr
    args['form'] = form
    args['username'] = auth.get_user(request).username

#    import pdb; pdb.set_trace()
    return render_to_response('create_task.html',args)

@login_required(login_url='/auth/login/')
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
            loger(auth.get_user(request), 'task_created', c.name, c, pr)

            return HttpResponseRedirect('/projector/project/{}'.format(parent.project_id))
    else:
        form = TaskForm()
    args = {}
    args.update(csrf(request))
    args['project'] = pr
    args['form'] = form
    args['parent'] = parent
    args['username'] = auth.get_user(request).username

#    import pdb; pdb.set_trace()

    return render_to_response('create_task.html',args)

@login_required(login_url='/auth/login/')
def task_show(request, task_id):
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=task.project.id)
    user = auth.get_user(request)
    real_time = 'not specified'
    if task.status == 'Finished':
        start_date = task.start_date
        if not task.start_date:
            start_date = task.create_date
        real_time = ((task.finish_date - start_date).total_seconds())/60/60
    form = TaskDoneForm()
    args = {}
    args.update(csrf(request))     # 4 task_done
    args['form'] = form
    args['project'] = project
    args['task'] = task
    args['username'] = user.username
    args['real_time'] = real_time
    if user in list(task.workers.all()):
        args['my_task']=True
    if user == task.creator:
        args['creator']=True
    loger(user, 'show_task', task.name, task, project)
    return render_to_response('task.html',args)

@login_required(login_url='/auth/login/')
def task_accept(request, task_id):
    user = auth.get_user(request)
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=task.project_id)
    task.workers.add(user)
    task.status = 'In work'
    if not task.start_date: # rewrite protection
        task.start_date = timezone.now()
    task.save()
    task_status_change(task_id, task.status, user)
    if project.status == 'dreams':
        project.status = 'In work'
        project.save()
        project_status_change(project.id, project.status, user)
    loger(user,'task_accept', task.name,task,project)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/auth/login/')
def task_stop(request, task_id):
    user = auth.get_user(request)
    task = Task.objects.get(id=task_id)
    task.workers.remove(user)
    task.save()
    if task.workers.count()==0:
        task.status = 'Freezed'
        task.save()
    task_status_change(task_id, task.status, user)
    loger(user, 'task_stop', task.name, task, task.project)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/auth/login/')
def task_done(request, task_id):
    task = Task.objects.get(id=task_id)
    user = auth.get_user(request)
    if request.method == 'POST':
        form = TaskDoneForm(request.POST)
        if form.is_valid():
            # import pdb; pdb.set_trace()
            digress = form.cleaned_data['digress']
            task.digress = digress
            task.status = 'Now check'
            task.save()
            task_status_change(task_id, task.status, auth.get_user(request))
            loger(user, 'task_done', task.name, task, task.project)
            return HttpResponseRedirect('/projector/task/{}'.format(task_id))
    return HttpResponseRedirect('/projector/task/{}'.format(task_id))

@login_required(login_url='/auth/login/')
def task_return(request, task_id):
    task = Task.objects.get(id=task_id)
    user = auth.get_user(request)
    task.status = 'Returned for revision'
    task.save()
    task_status_change(task_id, task.status, user)
    loger(user, 'task_return', task.name, task, task.project)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/auth/login/')
def task_finish(request, task_id):
    user = auth.get_user(request)
    task = Task.objects.get(id=task_id)
    now = timezone.now()
    task.status = 'Finished'
    task.finish_date = now
    task.save()
    task_status_change(task_id, task.status, user)
    loger(user, 'task_finished', task.name, task, task.project)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/auth/login/')
def all_tasks(reques):
    tasks = Task.objects.all()
#    import pdb; pdb.set_trace()
    args={}
    args['tasks'] = tasks
    args['username'] = auth.get_user(reques).username
    loger(auth.get_user(reques), 'show_all_tasks', 'all_tasks')
    return render_to_response('all_tasks.html', args)

@login_required(login_url='/auth/login/')
def my_tasks(request):
    user = auth.get_user(request)
    my_tasks = Task.objects.filter(workers__id=user.id).exclude(status='Finished')
    args={}
    args['tasks']=my_tasks
    args['username'] = user.username
    loger(user, 'show_my_tasks', 'my_tasks')
    return render_to_response('my_tasks.html',args)

@login_required(login_url='/auth/login/')
def my_projects(request):
    user = auth.get_user(request)
    #P. S: Mom and Dad this is Chasey
    my_tasks = Task.objects.filter(workers__id=user.id)
    my_projects = Project.objects.filter(task__workers__id=user.id).distinct()

    args={}
    args['my_projects']=my_projects
    args['username'] = user.username
    loger(user, 'show_my_projects', 'my_projects')

    return render_to_response('my_projects.html',args)

@login_required(login_url='/auth/login/')
def tests_page(request):
    from guardian.shortcuts import get_perms
    from guardian.shortcuts import get_objects_for_user
    user = auth.get_user(request)
    task = Project.objects.get(id=10)
    text = get_perms(user, task)
    text.append('----------------------------------')
    # text.append(str(get_objects_for_user(user, 'project.add_project')))
    perm = (get_objects_for_user(user, 'projector.change_task'))
    args={}
    args['perm']=perm
    args['text']=text
    args['my_projects'] = my_projects
    args['username'] = user.username
    request.session.set_expiry(60)
    request.session['pause'] = True
    return render_to_response('tests_page.html',args)

@login_required(login_url='/auth/login/')
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
            loger(user, u'write comment: {}'.format(c.comment), task.name, task, task.project)
            return HttpResponseRedirect('/projector/task/{}'.format(task_id))
    else:
        form = TaskCommentForm()
    args = {}
    args.update(csrf(request))
    args['task'] = task
    args['form'] = form
    args['username'] = user.username
    return render_to_response('task_comment.html',args)

@login_required(login_url='/auth/login/')
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
            loger(user, u'write comment: {}'.format(c.comment), project.name, project=project)
            return HttpResponseRedirect('/projector/project/{}'.format(project_id))
    else:
        form = ProjectCommentForm()
    args = {}
    args.update(csrf(request))
    args['project'] = project
    args['form'] = form
    args['username'] = user.username
    return render_to_response('project_comment.html',args)

@login_required(login_url='/auth/login/')
def welcome(request):
    if '57' in request.COOKIES:
        return HttpResponseRedirect('/projector/all/')
    else:
        response = render_to_response('welcome.html')
        response.set_cookie('57')
        return response

@login_required(login_url='/auth/login/')
def task_edit(request, task_id ):
    task = Task.objects.get(id=task_id)
#    import pdb; pdb.set_trace()
    user = auth.get_user(request)
    if request.POST:
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            loger(user, 'task_edit---after_editing---:{}; '.format(form.__dict__),
                  task.name, task, task.project)
            return HttpResponseRedirect('/projector/task/{}/'.format(task_id))
    else:
        form = TaskForm(instance=task)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['task'] = task
    args['user'] = user
    args['username']=user.username
    loger(user, 'task_edit---before_editing---:{}; '.format(task.__dict__),task.name, task, task.project)
    return render_to_response('task_edit.html',args)

@login_required(login_url='/auth/login/')
def comment_edit(request, comment_id):
    user = auth.get_user(request)
    comment = TaskComment.objects.get(id=comment_id)
    task_id = comment.task.id
    task = Task.objects.get(id=task_id)

    if request.POST:
        form = TaskCommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            loger(user, 'edit comment id-{} --after_editing--{} '.format(comment_id, form.__dict__), task.name, task, task.project)
            return HttpResponseRedirect('/projector/task/{}/'.format(task_id))
    else:
        form = TaskCommentForm(instance=comment)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['comment'] = comment
    args['user'] = user
    loger(user, 'edit comment id-{} --before_editing--{} '.format(comment_id, comment.__dict__), task.name, task, task.project)
    return render_to_response('comment_edit.html',args)

@login_required(login_url='/auth/login/')
def logs(request):
    user = auth.get_user(request)
    logs = ProjectorLog.objects.all()
    args={}
    args['username']=user.username
    args['logs']=logs
    return render_to_response('logs.html', args)