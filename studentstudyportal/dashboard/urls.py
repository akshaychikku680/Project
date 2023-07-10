from django.urls import path
from .views import *

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('notes',Note.as_view(),name='notes'),
    path('delete_note/<int:pk>',delete_note,name='delete_note'),
    path('notes_details/<int:pk>',NotesDetailView.as_view(),name='notes_details'),

    path('homework',Hwork.as_view(),name='homework'),
    path('update_homework/<int:pk>',update_homework,name='update_homework'),
    path('delete_homework/<int:pk>',delete_homework,name='delete_homework'),

    path('youtube',Youtube.as_view(),name='youtube'),

    path('todo',Todos.as_view(),name='todo'),
    path('update_todo/<int:pk>',update_todo,name='update_todo'),
    path('delete_todo/<int:pk>',delete_todo,name='delete_todo'),

    path('books',Book.as_view(),name='book'),

    path('dictionary',Dictionary.as_view(),name='dictionary'),

    path('wiki',Wiki.as_view(),name='wiki'), 

    path('conversion',Conversion.as_view(),name='conversion'),

]