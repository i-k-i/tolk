from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from achievement.models import Achievement, AchievementLogs, AchievementState
from forms import CreateAchievementForm, NewAchievementFrom
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import get_user


def achivement_loger(user, achievement):
    event = AchievementLogs(user=user, achievement=achievement)
    event.save()

@login_required()
def achivement_create(request,):
    user = request.user
    if request.POST:
        form = CreateAchievementForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.creator = user
            c.save()
            #achivement_loger(user, c)
            return redirect('/achievement/{}'.format(c.id))
    else:
        form = CreateAchievementForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    return render_to_response('achievement_create.html', args)

def achievement_show(request, achievement_id):
    achievement = Achievement.objects.get(id=achievement_id)
    args ={}
    args['achievement'] = achievement
    return render_to_response('achievement_show.html', args)

def achievement_all(request):
    achievements = Achievement.objects.all()
    args = {}
    args['achievements'] = achievements
    return render_to_response('achievement_all.html', args)

@login_required()
def achievement_log(request):
    log = AchievementLogs.objects.all()
    return render_to_response('achievement_log.html', {'log':log})

@login_required()
def achievement_new(request):
    if request.POST:
        form = NewAchievementFrom(request.POST)
        if form.is_valid():
            achiev = form.save(commit=False)
            achiev.quantity+=1
            achiev.save()
            achivement_loger(achiev.user, achiev.achievement)
            return redirect('/achievement/user/{}/'.format(achiev.user))
    else:
        form=NewAchievementFrom()

    args = {}
    args.update(csrf(request))
    args['form'] = form
#    import pdb; pdb.set_trace()

    return render_to_response('achievement_new.html',args)

def achievements_user(request, user_id):
    user = User.objects.get(id=user_id)
    achievements = AchievementState.objects.filter(user=user_id)
    args ={}
    args['achievements'] = achievements
    args['user'] = user
    print args
    return render_to_response('achievement_user.html', args)

