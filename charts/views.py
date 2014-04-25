from django.shortcuts import render
from django.http import HttpResponse
from charts.models import Issues
from django.db.models import Count
from django import forms

# Create your views here.
def index(request):
    top_assigned = Issues.objects.values_list('assigned_to').annotate(assigned_count=Count('assigned_to')).order_by('-assigned_count')[:10]
    print str(top_assigned)
    context = {
        'values': [
            ['behaviour',Issues.objects.filter(type='behavior').count()],
            ['resource',Issues.objects.filter(type='resource usage').count()],
            ['crash',Issues.objects.filter(type='crash').count()],
            ['enhancement',Issues.objects.filter(type='enhancement').count()],
            ['security',Issues.objects.filter(type='security').count()]
        ],
        'values_2': [
            ['open',Issues.objects.filter(status='open').count()],
            ['closed',Issues.objects.filter(status='closed').count()],
            ['pending',Issues.objects.filter(status='pending').count()],
            ['languishing',Issues.objects.filter(status='languishing').count()]
        ],
        'values_3': [
            [top_assigned[0][0],top_assigned[0][1]],
            [top_assigned[1][0],top_assigned[1][1]],
            [top_assigned[2][0],top_assigned[2][1]],
            [top_assigned[3][0],top_assigned[3][1]],
            [top_assigned[4][0],top_assigned[4][1]],
            [top_assigned[5][0],top_assigned[5][1]],
            [top_assigned[6][0],top_assigned[6][1]],
            [top_assigned[7][0],top_assigned[7][1]],
            [top_assigned[8][0],top_assigned[8][1]],
            [top_assigned[9][0],top_assigned[9][1]]
        ]
    }

    return render(request, 'charts/index.html',context)

#def add_new(request):
#    context = {}
#    return render(request, 'charts/index.html',context)
    