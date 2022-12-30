from django.shortcuts import render
from django.http import HttpRequest
import threading 

from .forms import EmailForm
from .models import Subscribers
from .epic_bot.notify_user import notify_all_subs
from .epic_bot.fetch_promotionalOffers_games import fatch_promo_game


def home(request:HttpRequest):
    form = EmailForm()
    error = False
    submitted = False
    # notify_all_subs()
    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            submitted = True
            Subscribers.objects.get_or_create(email=form.data.get('email'))
            # th = threading.Thread(target=get_active_promo_game_and_notify_all_subs,name='home_page_th')
            # th.start()
            # fatch_promo_game()
        else:
            error = True
    return render(request,'home.html',context={'has_error':error,'submitted':submitted})