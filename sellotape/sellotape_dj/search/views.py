from django.shortcuts import render
from django.db.models import Q
from main_app.models import Profile, Stream

from itertools import chain
 

# Create your views here.

def search(request):
	view_url = 'search/view.html'

	query = request.GET.get('search', None)

	stream_results_title = Stream.objects.filter(title__icontains=query)
	stream_results_description = Stream.objects.filter(description__icontains=query)

	stream_results = chain(
		stream_results_title,
		stream_results_description,
		)
	length_streams = len(stream_results_title)+len(stream_results_description)

	profile_results_username = Profile.objects.filter(user__username__icontains=query)
	profile_results_firstname = Profile.objects.filter(user__first_name__icontains=query)
	profile_results_lastname = Profile.objects.filter(user__last_name__icontains=query)

	profile_results = chain(
		profile_results_username,
		profile_results_firstname,
		profile_results_lastname,
		)
	length_profiles = len(profile_results_username) + len(profile_results_firstname) + len(profile_results_lastname)
	
    # combine querysets 
	queryset_chain = chain(
		stream_results,
		profile_results
		)
	if queryset_chain is not None:
		if stream_results is not None or profile_results is not None:
				qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
    
	count = length_streams + length_profiles
	context = {
        'qs': qs,
        'query': query,
        'count': count,
    }
	print(context)
	return render(request, 'sellotape/search.html', context)