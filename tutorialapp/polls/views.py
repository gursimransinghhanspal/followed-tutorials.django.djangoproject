from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list': latest_question_list,
	}

	# Method 1: use loader, template.render
	# template = loader.get_template('polls/index.html')
	# return HttpResponse(template.render(context, request))

	# Method 2: use render
	return render(request, 'polls/index.html', context)


def detail(request, question_id):
	# Method 1: try-except with Http404
	# try:
	# 	question = Question.objects.get(pk = question_id)
	# except Question.DoesNotExist:
	# 	raise Http404("Question does not exist")

	# Method 2: get_object_or_404
	question = get_object_or_404(Question, pk = question_id)
	return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
	return HttpResponse("You are looking at results of question %s." % question_id)


def vote(request, question_id):
	return HttpResponse("You are voting on question %s." % question_id)
