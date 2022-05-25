from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('UpdateTickets/<ticket_id>', views.UpdateTickets, name="UpdateTickets"),
    path('DeleteTickets/<ticket_id>', views.DeleteTickets, name="DeleteTickets"),
    path('GetTickets', views.GetTickets, name='GetTickets' ),
    path('sendTickets', views.sendTickets, name='getAlltickets'),
    path('tickets', views.tickets, name='tickets'),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('update/<ticket_id>', views.update, name="update")
]
