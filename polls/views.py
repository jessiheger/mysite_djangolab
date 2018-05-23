from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# To call the view, we need to map it to a URL - and for this we need a URLconf (create a file called urls.py in the poll directory)
# The get_object_or_404() function ^ takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function of the model’s manager. It raises Http404 if the object doesn’t exist.
#The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

# Each generic view needs to know what model it will be acting upon. This is provided using the model attribute.
# The DetailView generic view expects the primary key value captured from the URL to be called "pk", so we’ve changed question_id to pk for the generic views.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # template_name tells Django to use a specific template
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    # ^ tells index view to use template from polls/index.html
    # ^ loads the template called polls/index.html and passes it a context.
    # 'return render()' is a common shortcut to load a template, fill a context and return an HttpResponse object with the result of the rendered template


# These views take an argument:
# Must be added to polls.urls

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# We specify the template_name for the results list view – this ensures that the results view and the detail view have a different appearance when rendered, even though they’re both a DetailView behind the scenes.

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST lets you access submitted data by key name. Here, it request.POST['choice'] returns the ID of a selected choice a a string.
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # HttpResponseRedirect always takes 1 argument: the URL to which the user will be redirected
        # reverse() is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view.
        # in this case, reverse() will return a string like '/polls/3/results' where 3 is the question.id
        # this redirected URL will then call the 'results' view to display the final page