from django.contrib import admin
from django.urls import path
from . import views
from .views import NoteView

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login_user, name = 'login'), #login_user so it does not conflict with login function import from django
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register, name ='register'),
    path('records/', views.records, name ='records'),
    path('export/<str:format>/', views.export_data, name='export_data'),
    path('details/<int:ID>/', views.details, name='details'),
    path('delete_record/<int:ID>/', views.delete_record, name='delete_record'),
    path('update_record/<int:ID>/', views.update_record, name='update_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('notes/<int:ID>/', NoteView.as_view(), name='notes'),
    path('notes/<int:ID>/edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/<int:ID>/delete_note/<int:note_id>/',views.delete_note, name='delete_note'),
] 