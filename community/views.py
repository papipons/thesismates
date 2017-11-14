from django.shortcuts import render, redirect
from django.contrib.auth.decorators import (
	login_required
)

from core import utils as core_u
from . import forms as com_f
from . import utils as com_u
from core import utils as core_u
from .models import Question, Question_Answer
from django_ajax.decorators import ajax
from django.http import HttpResponseForbidden

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def community(request):
	context = {}
	context['questions'] = Question.objects.filter(accepted=True).order_by('-created_date')
	context['is_admin'] = core_u.is_admin(request.user)
	context['search_form'] = com_f.SearchForm()
	context['ask_form'] = com_f.AskQuestionForm()
	context['community'] = True

	if core_u.is_admin(request.user):
		pending_questions = Question.objects.filter(accepted=None)
		pending_answers = Question_Answer.objects.filter(accepted=None)
	else:
		pending_questions = Question.objects.filter(accepted=None,asked_by=request.user)
		pending_answers = Question_Answer.objects.filter(accepted=None, answered_by=request.user)


	if pending_questions:
		context['pending_qs'] = pending_questions.order_by('-created_date')

	if pending_answers:
		context['pending_as'] = pending_answers.order_by('-created_date')

	return render(request, 'community/community.html', context)

# --------------------------------------------------------------------

def question(request, id, slug):
	context = {}
	question = Question.objects.get(pk=id)
	if question.accepted == True:
		context['question'] = question
		context['answers'] = Question_Answer.objects.filter(
			question__pk=id, accepted=True).order_by('-created_date')
		context['answer_form'] = com_f.AnswerQuestionForm()
		context['community'] = True
		return render(request, 'community/question.html', context)
	else:
		return HttpResponseForbidden()


# --------------------------------------------------------------------

@ajax
def ask_question(request):
	form = com_f.AskQuestionForm(request.POST)

	if form.is_valid():
		question_object = form.save_question(request.user)
		return redirect(community)
	else:
		print "invalid"

# --------------------------------------------------------------------

def accept(request, response, id):
	if response == "question":
		q = Question.objects.filter(pk=id)
		q_obj = q.get()
		q.update(accepted=True)
		return redirect(question, q_obj.id, q_obj.slug)
	if response == "answer":
		a = Question_Answer.objects.filter(pk=id)
		a_obj = a.get()
		a.update(accepted=True)
		return redirect(question, a_obj.question.id, a_obj.question.slug)

# --------------------------------------------------------------------

def reject(request, response, id):
	if response == "question":
		q = Question.objects.filter(pk=id)
		q.delete()
		return redirect(community)
	if response == "answer":
		a = Question_Answer.objects.filter(pk=id)
		a.delete()
		return redirect(community)

# --------------------------------------------------------------------

@ajax
def get_search(request):
	form = com_f.SearchForm(request.POST)
	context = {}
	if form.is_valid():
		context['questions'] = com_u.get_search(form).order_by('-created_date')
		words = request.POST.get('search')
		keywords = words.split()
		context['keywords'] = keywords

		return render(request, 'community/search.html', context)

# --------------------------------------------------------------------

@ajax
def answer(request, id, slug):
	form = com_f.AnswerQuestionForm(request.POST)

	if form.is_valid():
		question_object = Question.objects.get(pk=id, slug=slug)
		form.save_answer(question_object, request.user)
		return redirect(question, id, slug)
	else:
		print "invalid"
