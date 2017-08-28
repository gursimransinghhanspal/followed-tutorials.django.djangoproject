from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F

from .models import Choice, Question


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
	question = get_object_or_404(Question, pk = question_id)
	return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)

	try:
		selected_choice = Choice.objects.get(pk = request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		# There is a possibility of a race condition while updating values in a db.
		# selected_choice.votes += 1
		# selected_choice.save()

		# Use F() to get around race conditions
		selected_choice.votes = F('votes') + 1
		selected_choice.save()

		# NOTE: F() objects persist after save()
		# To stop it from running on every save just refresh the object from db again
		selected_choice.refresh_from_db()

		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
