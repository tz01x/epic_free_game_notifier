from django.shortcuts import render
from django.http import HttpRequest


from .forms import EmailForm
from .models import Subscribers
from .epic_bot.notify_user import notify_all_subs
from .epic_bot.fetch_promotionalOffers_games import fetch_promo_game


def home(request:HttpRequest):
    form = EmailForm()
    error = False
    submitted = False
    if request.method == 'POST':
        notify_all_subs()  
        form = EmailForm(data=request.POST)
        if form.is_valid():
            submitted = True
            obj,created = Subscribers.objects.get_or_create(email=form.data.get('email'))
            if created:
                obj.is_active = True
                obj.save()
        else:
            error = True
    return render(request,'home.html',context={'has_error':error,'submitted':submitted})


def unsubscribe(request:HttpRequest):
    if request.GET.get('id'):
        Subscribers.objects.filter(id=request.GET.get('id')).update(is_active=False)
    return render(request,'unsubscribe.html')