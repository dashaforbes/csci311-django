from django.shortcuts import render
from django.http import HttpResponse
from charts.models import Issues

# Create your views here.
def index(request):
    behavior_val = len(Issues.objects.filter(type='behavior'))
    resource_val = len(Issues.objects.filter(type='resource usage'))
    crash_val = len(Issues.objects.filter(type='crash'))
    enhancement_val = len(Issues.objects.filter(type='enhancement'))
    security_val = len(Issues.objects.filter(type='security'))
    context = {
        'values': [
            ['behaviour',behavior_val],
            ['resource',resource_val],
            ['crash',crash_val],
            ['enhancement',enhancement_val],
            ['security',security_val]
        ]
    }

    return render(request, 'charts/index.html',context)
