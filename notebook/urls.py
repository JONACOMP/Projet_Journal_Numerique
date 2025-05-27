from django.urls import path
from .views.views import *

app_name = "notebook"

urlpatterns = [    
  path('new/', NewNoteView.as_view(), name='new_note'),
  path('notes/<uuid:pk>/', NoteDetailView.as_view(), name='detail'),
  path('note/<uuid:pk>/delete/', note_delete, name='deletenote'),
  path('notebooks/<uuid:pk>/delete/', notebook_delete, name='delete'),

]
