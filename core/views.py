from typing import List
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
import random

from .models import Category, Question, Answer


def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.GET.get('category'):
        return redirect(f"quiz/?category={request.GET.get('category')}")
    return render(request, 'home.html', context)


def get_quiz(request):
    questions = Question.objects.all()
    if request.GET.get('category'):
        questions = questions.filter(category__category__icontains=request.GET.get('category'))
    data = []

    random.shuffle(questions)

    for question in questions:
        data.append({
            "question": question.question,
            "answers": question.get_answer()
        })

    payload = {'data': data}

    return JsonResponse(payload, json_dumps_params={'indent': 2})


##################
def quiz(request, question_id=None):
    if question_id is None:
        question = Question.objects.first()
    else:
        question = get_object_or_404(Question, id=question_id)

    if question:
        answer = None
        if request.method == 'POST':
            selected_answer_id = request.POST.get('answer')
            selected_answer = get_object_or_404(Answer, pk=selected_answer_id)

            if selected_answer.is_correct:
                question = Question.objects.filter(pk__gt=question.pk).first()
                answer = None
            else:
                answer = selected_answer
        answers = question.answers.all()

        return render(request, 'quiz.html', {
            'question': question,
            'answers': answers,
            'selected_answer': answer,
        })
    return render(request, 'quiz.html')

def get_next_question(request):
    current_question_id = request.GET.get('current_question_id')
    current_question = get_object_or_404(Question, pk=current_question_id)
    next_question = Question.objects.filter(pk__gt=current_question.pk).first()

    if next_question:
        data = {'question_id': next_question.pk}
    else:
        data = {'question_id': None}

    return JsonResponse(data)


def mymodel_detail(request, pk):
    mymodel = get_object_or_404(Question, pk=pk)
    context = {'question': mymodel}
    return render(request, 'question_detail.html', context)

#+=====================================

def QuizView(request):
    if request.method == 'POST':
        # Get the selected answer from the form submission
        selected_answer_id = request.POST.get('answer')
        selected_answer = Answer.objects.get(id=selected_answer_id)
        # Check if the selected answer is correct
        question_list = request.session.get('question_list', [])
        if selected_answer.is_correct:
            # If the answer is correct, add to the score and add the question ID to the list of correctly answered questions
            request.session['score'] += 1
            request.session['correct_answers'].append(selected_answer.question.id)
            # Get the next question from the list
            
            if question_list:
                next_question_id = question_list.pop(0)
                request.session['question_list'] = question_list
                # Render the template with the next question
                next_question = Question.objects.get(id=next_question_id)
                return render(request, 'quiz.html', {'question': next_question})
            else:
                # If there are no more questions, display the "quiz finished" template with the score and list of correct answers
                score = request.session.get('score', 0)
                final_score = score/request.session['questions_amount']*100
                correct_answers = request.session.get('correct_answers', [])
                return render(request, 'quiz_finished.html', {'score': score, 'final_score': final_score})
        else:
            # If the answer is incorrect
            if question_list:
                next_question_id = question_list.pop(0)
                request.session['question_list'] = question_list
                # Render the template with the next question
                next_question = Question.objects.get(id=next_question_id)
                return render(request, 'quiz.html', {'question': next_question})
            else:
                # If there are no more questions, display the "quiz finished" template with the score and list of correct answers
                
                score = request.session.get('score', 0)
                final_score = score/request.session['questions_amount']*100
                return render(request, 'quiz_finished.html', {'score': score, 'final_score': final_score})
    else:
        # If this is the first time loading the page, generate the question list and display the first question
        question_list = Question.objects.values_list('id', flat=True)
        if request.GET.get('category'):
            question_list = list(question_list.filter(category__category__icontains=request.GET.get('category')))
        else:
            return render(request, 'quiz.html')
        random.shuffle(question_list)
        request.session['question_list'] = question_list
        request.session['score'] = 0
        request.session['correct_answers'] = []
        request.session['questions_amount'] = len(question_list)
        first_question_id = question_list.pop(0)
        first_question = Question.objects.get(id=first_question_id)
        return render(request, 'quiz.html', {'question': first_question})
    

def question_details(request):
    # Get the selected answer from the form submission
    if request.method == 'POST':
        button_value = request.POST.get('button')
        if button_value == 'get_details':
            question = Question.objects.get(id=1)
            selected_answer_id = request.POST.get('answer')
            selected_answer = Answer.objects.get(id=selected_answer_id)
            question_list = request.session.get('question_list', [])
            # Check if the selected answer is correct
            if selected_answer.is_correct:
                return JsonResponse('Your answer is correct!')
            # If the submitted answer is incorrect, return the correct answer
            correct_answer = question.answer_set.filter(is_correct=True).first()
            context = {'correct_answer': correct_answer}
            return render(request, 'question_detail.html', context)
        elif button_value == 'next_question':
            return JsonResponse('Next question...')

    return render(request, 'quiz.html')


def QuizFinishedView(request):
    return render(request, 'quiz_finished.html')


#=========== PROMPT

# Create a Django quiz app, with Question and Answer model, the view should render only the first question, 
# and when submit the answer, if the answer is correct, show the next question, if it is not correct, show the correct 
# answer and a button to show the next question, when the questions are over, show the percentage of questions answered successfully

#Create a Django quiz app, with Question and Answer model, the view should render only the first question and when submit the answer, if the answer is incorrect, show the correct answer, if is correct show the next question, when the questions are over, show the percentage of questions answered successfully

# but when is incorrect, you are not looking for the correct answer, it is just returning the answer that was submited