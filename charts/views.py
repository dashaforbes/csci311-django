from django.shortcuts import render
from django.http import HttpResponse
from charts.models import Issue
from django.db.models import Count
from django import forms

# Create your views here.
def index(request):
    top_assigned = Issue.objects.values_list('assigned_to').annotate(assigned_count=Count('assigned_to')).order_by('-assigned_count')[:10]
    print str(top_assigned)
    context = {
        'values': [
            ['behaviour',Issue.objects.filter(type='behavior').count()],
            ['resource',Issue.objects.filter(type='resource usage').count()],
            ['crash',Issue.objects.filter(type='crash').count()],
            ['enhancement',Issue.objects.filter(type='enhancement').count()],
            ['security',Issue.objects.filter(type='security').count()]
        ],
        'values_2': [
            ['open',Issue.objects.filter(status='open').count()],
            ['closed',Issue.objects.filter(status='closed').count()],
            ['pending',Issue.objects.filter(status='pending').count()],
            ['languishing',Issue.objects.filter(status='languishing').count()]
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
    