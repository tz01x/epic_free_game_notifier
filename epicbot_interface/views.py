from django.shortcuts import render
from django.http import HttpRequest
import threading

from .forms import EmailForm
from .models import Subscribers
from .epic_bot.notify_user import notify_sub_user



def home(request:HttpRequest):
    form = EmailForm()
    error = False
    submitted = False
    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            submitted = True
            obj, created = Subscribers.objects.get_or_create(email=form.data.get('email'))
            if created:
                obj.is_active = True
                obj.save()
            th = threading.Thread(target=notify_sub_user,args=([obj],),daemon=True)
            th.start()
        else:
            error = True
    return render(request,'home.html',context={'has_error':error,'submitted':submitted})


def unsubscribe(request:HttpRequest):
    if request.GET.get('id'):
        Subscribers.objects.filter(id=request.GET.get('id')).update(is_active=False)
    return render(request,'unsubscribe.html')