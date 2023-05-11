from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/get-quiz/', views.get_quiz, name='get_quiz'),
    path('quiz/', views.QuizView, name='quiz'),
    path('quiz/<int:question_id>/', views.quiz, name='quiz'),
    path('quiz/question_detail/', views.question_details, name='question_details'),
    path('quiz/finished/', views.QuizFinishedView, name='quiz_finished'),
]