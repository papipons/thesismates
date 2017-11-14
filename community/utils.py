import operator
from django.db.models import Q
from . import models as comm_m

# --------------------------------------------------------------------

def get_search(form):
	to_search = form.cleaned_data['search']
	keywords = to_search.split()

	result = comm_m.Question.objects.filter(
		reduce(operator.or_, (
				Q(title__icontains=x, accepted=True) for x in keywords)
			)
	)

	return result
