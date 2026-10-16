from django.urls import path
from . import views

urlpatterns = [
    path('app/', views.webapp_view, name='webapp'),
    path('api/collect/', views.collect_earnings, name='collect_earnings'),
    path('api/buy/', views.buy_bird, name='buy_bird'),
]
