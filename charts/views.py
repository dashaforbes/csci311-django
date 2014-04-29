from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from charts.models import Issue, People, IssueForm, IssueEditForm, LoginForm, RegisterForm, Commit, Developer
from django.db.models import Count
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    top_assigned = Issue.objects.values_list('assigned_to').annotate(assigned_count=Count('assigned_to')).order_by('-assigned_count')[:10]
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

@login_required
def add_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            creator = People.objects.get(username=request.user.username)
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

def index_redirect(request):
    return HttpResponseRedirect('/charts/')

def issue_index(request):
    issues = Issue.objects.order_by('-activity').all()
    context = {
        'issues':issues,
        'stats': {
            'amount':Issue.objects.all().count(),
            'contrib':Issue.objects.values_list('creator').annotate(contrib_count=Count('creator')).count(),
            'open':Issue.objects.filter(status='OP').count(),
            'closed':Issue.objects.filter(status='CL').count(),
            'pending':Issue.objects.filter(status='PE').count(),
            'languish':Issue.objects.filter(status='LA').count()
        }
    }
    return render(request, 'charts/issues/index.html', context)

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if str(issue.creator) == request.user.username or request.user.groups.filter(name='Project Manager'):
        edit = True
    else:
        edit = False
    context = {
        'issue':issue,
        'edit':edit
    }
    return render(request, 'charts/issues/detail.html', context)

@login_required
def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    redirect = '/charts/issues/' + issue_id + '/'
    if request.user.username != str(issue.creator) and not request.user.groups.filter(name='Project Manager'):
        return HttpResponseRedirect(redirect)    

    if request.method == 'POST':
        form = IssueEditForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            issue.components = d['components']
            issue.versions = d['versions']
            issue.nosy_list = d['nosy_list']
            issue.save()
            Issue.objects.filter(id=issue_id).update(
                title=d['title'],
                assigned_to=d['assigned_to'],
                message_count=d['message_count'],
                type=d['type'],
                stage=d['stage'],
                status=d['status'],
                priority=d['priority'],
            )
            return HttpResponseRedirect(redirect)
    else:
        form = IssueEditForm(instance=issue)

    return render(request, 'charts/issues/edit.html', {
        'form':form,
        'issue':issue,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = authenticate(username=d['username'], password=d['password'])
            if user is not None:
                login(request, user)
                if d['next']:
                    return HttpResponseRedirect(d['next'])
                else:
                    return HttpResponseRedirect('/charts/')
            else:
                messages.error(request, "Invalid login details :(")
     
    else:
        next = request.GET.get('next')
        form = LoginForm(initial={'next':next})
    
    return render(request, 'charts/account/login.html', {
        'form':form,
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/charts/')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            #try:
            user = User.objects.create_user(username=d['username'], password=d['password'])
            g = Group.objects.get(name=d['group'])
            g.user_set.add(user)
            p = People(username=d['username'])
            p.save()
            user = authenticate(username=d['username'], password=d['password'])
            login(request, user)
            return HttpResponseRedirect('/charts/')
            #except: 
            messages.error(request, d['username'])

    else:
        form = RegisterForm(initial={'group':'Contributor'})
     

    return render(request, 'charts/account/register.html', {
        'form':form,
    })

def people_index(request):
    people = People.objects.all().annotate(assigned_count = Count('assigned_to')).annotate(created_count = Count('creator')).annotate(nosy_count = Count('nosy_list')).order_by('-created_count')
    context = {
        'people':people
    }
    return render(request, 'charts/people/index.html', context)

def person_detail(request, person_id):
    person = get_object_or_404(People, pk=person_id)
    context = {
        'person':person,
        'stats': {
            'created_count':Issue.objects.filter(creator=person.username).count(),
            'assigned_count':Issue.objects.filter(assigned_to=person.username).count(),
            'nosy_count':Issue.objects.filter(nosy_list=person.username).count(),
        }
    }
    return render(request, 'charts/people/detail.html', context)

def commits_index(request):
    commits = Commit.objects.all().order_by('-time')
    context = {
        'commits':commits,
        'stats': {
            'count':Commit.objects.all().count()
        }
    }

    return render(request, 'charts/commits/index.html', context)