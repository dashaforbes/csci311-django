from django.shortcuts import render
from django.http import HttpResponse
from charts.models import Issue, People, IssueForm
from django.db.models import Count
from django import forms
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    top_assigned = Issue.objects.values_list('assigned_to').annotate(assigned_count=Count('assigned_to')).order_by('-assigned_count')[:10]
    print str(top_assigned)
    context = {
        'values': [
            ['behaviour',Issue.objects.filter(type='BE').count()],
            ['resource',Issue.objects.filter(type='RE').count()],
            ['crash',Issue.objects.filter(type='CR').count()],
            ['enhancement',Issue.objects.filter(type='EN').count()],
            ['security',Issue.objects.filter(type='SE').count()]
        ],
        'values_2': [
            ['open',Issue.objects.filter(status='OP').count()],
            ['closed',Issue.objects.filter(status='CL').count()],
            ['pending',Issue.objects.filter(status='PE').count()],
            ['languishing',Issue.objects.filter(status='LA').count()]
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

def add_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            creator = People.objects.get(username="Test")
            i = Issue(
                title=data['title'],
                creator=creator,
                type=data['type'],
                assigned_to=data['assigned_to'],
                priority=data['priority']
            )
            i.save()
            return HttpResponseRedirect('/charts/')
    else:
        form = IssueForm()

    return render(request, 'charts/issues/add.html',{
        'form': form,
    })

def issue_index(request):
    return render(request, 'charts/issues/index.html', {})

def index_redirect(request):
    return HttpResponseRedirect('/charts/')
    