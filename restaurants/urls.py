from django.urls import path

from restaurants import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]
