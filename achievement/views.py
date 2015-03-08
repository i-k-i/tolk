from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from achievement.models import Achievement, AchievementLogs, AchievementState, AchievementKit, QuantityAchievements
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
            state = AchievementState.objects.filter(achievement=achiev.achievement, user=achiev.user)
            if state:
                state[0].quantity+=1
                state[0].save()
            else:
                achiev.quantity+=1
                achiev.save()
                achivement_loger(achiev.user, achiev.achievement)
            return redirect('/achievement/user/{}/'.format(achiev.user_id))
    else:
        form = NewAchievementFrom()

    args = {}
    args.update(csrf(request))
    args['form'] = form
#    import pdb; pdb.set_trace()

    return render_to_response('achievement_new.html',args)

def achievements_user(request, user_id):
    user = User.objects.get(id=user_id)
    achievements = AchievementState.objects.filter(user=user_id)
#    import pdb; pdb.set_trace()
    args ={}
    args['achievements'] = achievements
    args['user'] = user
    return render_to_response('achievements_user.html', args)

def search_kit(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    args = {}
    kits = {}
#    {'achievement_kits':kits}
    found_kits_ = AchievementKit.objects.filter(name__contains=search_text)
    for kit in found_kits_:
        achieves = QuantityAchievements.objects.filter(kit=kit)
        kits[kit.name] = achieves
    args['achievement_kits'] = kits
    # print '-----'
    # import pdb; pdb.set_trace()
    print request.session.session_key
    return render_to_response('search_kit.html', args)

def kits(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('achievement_kits.html',args)

