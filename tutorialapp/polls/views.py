from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'


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
