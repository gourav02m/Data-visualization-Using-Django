from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact,name='contact'),
    path('home/',views.greetings, name='home'),
    path('home/search',views.search),
    path('about',views.about,name='about'),
    path('faq',views.faq,name='faq'),
    path('pricing',views.pricing,name='pricing')
]