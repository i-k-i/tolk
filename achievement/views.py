from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from achievement.models import Achievement, AchievementLogs, AchievementState
from forms import AchievementForm
from django.shortcuts import redirect
from django.core.context_processors import csrf


def achivement_loger(user, achievement):
    event = AchievementLogs(user=user, achievement=achievement)
    event.save()

@login_required()
def achivement_create(request,):
    user = request.user
    if request.POST:
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.creator = user
            c.save()
            achivement_loger(user, c)
            return redirect('achivement/{}'.format(c.id))
    else:
        form = AchievementForm()
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
    achievement_all = Achievement.objects.all()
    return render_to_response('achievement_all.html', achievement_all)

@login_required()
def achievement_log(request):
    log = AchievementLogs.objects.all()
    return render_to_response('achievement_log.html', log)
