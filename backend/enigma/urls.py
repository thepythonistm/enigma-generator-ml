from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_enigma_view, name='generate_enigma'),
    path('answer/<int:riddle_id>/', views.get_answer_view, name='get_answer'),
]
