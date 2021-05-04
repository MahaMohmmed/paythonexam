from django.urls import path
from . import views

urlpatterns = [
        path('', views.index),
        path('register', views.register),
        path('wishes', views.wishes),
        path('login', views.login),
        path('goback',views.index2),
        path('wishes/new', views.new_wish),
        path('wishes/create' ,views.creat_wish),
        path('wishes/<int:w_id>/edit', views.edit_wish),
        path('wishes/<int:w_id>/update', views.update_wish),
        path('wishes/<int:w_id>/delete', views.delete_wish),
        path('wishes/<int:w_id>/granted', views.granted_wish),
        path('wishes/states', views.states),
        path('wishes/<int:w_id>/like',views.like),


]
