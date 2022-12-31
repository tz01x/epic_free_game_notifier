from django.urls import path
from .views import home,unsubscribe


urlpatterns = [
    # path("admin/", admin.site.urls),
    path('',home,name='home'),
    path('unsubscribe/',unsubscribe,name='unsubscribe'),
]