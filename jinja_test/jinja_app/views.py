from django.shortcuts import render
from .models import Candidate

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'jinja2/candidate_list.html', {'candidates': candidates})
