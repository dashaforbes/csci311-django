from django.db import models
from django.forms import ModelForm, Form, CharField, PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

# Create your models here.

class Component(models.Model):
    name = models.CharField(primary_key=True, max_length=30)

    def __unicode__(self):
        return self.name

class Version(models.Model):
    version = models.CharField(primary_key=True, max_length=3)

    def __unicode__(self):
        return self.version
    
class People(models.Model):
    username = models.CharField(primary_key=True, max_length=100)

    def __unicode__(self):
        return self.username

class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(People, related_name='creator')
    title = models.CharField(max_length=250)
    assigned_to = models.ForeignKey(People, blank=True, null=True, related_name='assigned_to')
    message_count = models.IntegerField(default=0)
    components = models.ManyToManyField(Component, blank=True, null=True, related_name='components')
    versions = models.ManyToManyField(Version, blank=True, null=True, related_name='versions')
    nosy_list = models.ManyToManyField(People, blank=True, null=True, related_name='nosy_list')

    NONE = 'NA'

    BEHAVIOR = 'BE'
    CRASH = 'CR'
    COMPILE = 'CO'
    RESOURCE = 'RE'
    SECURITY = 'SE'
    PERFORMANCE = 'PE'
    ENHANCEMENT = 'EN'
    TYPE_CHOICES = (
        (NONE, 'none'),
        (BEHAVIOR, 'behavior'),
        (CRASH, 'crash'),
        (COMPILE, 'compile error'),
        (RESOURCE, 'resource usage'),
        (SECURITY, 'security'),
        (PERFORMANCE, 'performance'),
        (ENHANCEMENT, 'enhancement')
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NONE)
    
    TEST_NEEDED = 'TN'
    NEEDS_PATCH = 'NP'
    PATCH_REVIEW = 'PR'
    COMMIT_REVIEW = 'CR'
    RESOLVED = 'RE'
    STAGE_CHOICES = (
        (NONE, 'none'),
        (TEST_NEEDED, 'test needed'),
        (NEEDS_PATCH, 'needs patch'),
        (PATCH_REVIEW, 'patch review'),
        (COMMIT_REVIEW, 'commit review'),
        (RESOLVED, 'resolved')
    )
    stage = models.CharField(max_length=2, choices=STAGE_CHOICES, default=NONE)

    OPEN = 'OP'
    CLOSED = 'CL'
    LANGUISHING = 'LA'
    PENDING = 'PE'
    STATUS_CHOICES = (
        (OPEN, 'open'),
        (CLOSED, 'closed'),
        (LANGUISHING, 'languishing'),
        (PENDING, 'pending')
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=OPEN)

    LOW = 'LO'
    NORMAL = 'NO'
    HIGH = 'HI'
    CRITICAL = 'CR'
    DEFERRED_BLOCKER = 'DE'
    RELEASE_BLOCKER = 'RE'
    PRIORITY_CHOICES = (
        (LOW, 'low'),
        (NORMAL, 'normal'),
        (HIGH, 'high'),
        (CRITICAL, 'critical'),
        (DEFERRED_BLOCKER, 'deferred blocker'),
        (RELEASE_BLOCKER, 'release blocker')
    )
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default=NORMAL)

    def __unicode__(self):
        return unicode(self.title)

class Developer(models.Model):
    email = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Commit(models.Model):
    hash = models.CharField(max_length=50,primary_key=True)
    author = models.ForeignKey(Developer)
    time = models.DateTimeField('commit time')
    
    def __unicode__(self):
        return self.hash

class IssueForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = '/charts/issues/add/'
        self.helper.layout = Layout(
            Row(
                Div(
                    'title',
                    css_class = 'form-group col-xs-12'
                ),
                Div(
                    'assigned_to',
                    css_class = 'form-group col-xs-12'
                ),
                Div(
                    'nosy_list',
                    css_class = 'form-group col-xs-12'
                )
            ),
            Row(
                Div(
                    'type',
                    css_class = 'form-group col-xs-12 col-sm-6 col-md-6 col-lg-6'
                ),
                Div(
                    'priority',
                    css_class = 'form-group col-xs-12 col-sm-6 col-md-6 col-lg-6'
                ),
                Div(
                    'components',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-6 col-lg-6',
                ),
                Div(
                    'versions',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-6 col-lg-6',
                ),
            ),          
            Row(
                FormActions(
                    Submit('submit', 'Add', css_class='button btn-primary col-xs-12 col-sm-12 col-md-2 col-lg-1')
                )   
            )
        )

    class Meta:
        model = Issue
        exclude = ('creator','stage','status','message_count')

class IssueEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Div(
                    'title',
                    css_class = 'form-group col-xs-12'
                ),
                Div(
                    'assigned_to',
                    css_class = 'form-group col-xs-12'
                ),
                Div(
                    'nosy_list',
                    css_class = 'form-group col-xs-12'
                )
            ),
            Row(
                Div(
                    'type',
                    css_class = 'form-group col-xs-12 col-sm-6 col-md-6 col-lg-6'
                ),
                Div(
                    'priority',
                    css_class = 'form-group col-xs-12 col-sm-6 col-md-6 col-lg-6'
                ),
                Div(
                    'components',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-6 col-lg-6',
                ),
                Div(
                    'versions',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-6 col-lg-6',
                ),
                Div(
                    'stage',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-4 col-lg-4',
                ),
                Div(
                    'status',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-4 col-lg-4',
                ),
                Div(
                    'message_count',
                    css_class = 'form-group col-xs-12 col-sm-12 col-md-4 col-lg-4',
                ),
            ),          
            Row(
                FormActions(
                    Submit('submit', 'Save', css_class='button btn-primary col-xs-12 col-sm-12 col-md-2 col-lg-1')
                )   
            )
        )

    class Meta:
        model = Issue
        exclude = ('creator',)


class LoginForm(Form):
    username = CharField(
        label = "Username",
        max_length = 100,
        required = True,
    )

    password = CharField(
        label = "Password",
        max_length = 100,
        required = True,
        widget = PasswordInput,
    )
    
    next = CharField(
        max_length=100,
        required = False,
        label = ''
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/charts/account/login/'
        self.helper.label_class = 'col-xs-12 col-md-1'
        self.helper.field_class = 'col-xs-12 col-md-5'
        self.helper.layout = Layout(
            'username',
            'password',
            StrictButton('Login', css_class='btn-primary col-md-offset-1', type='submit'),
            HTML('<a href="/charts/" class="btn btn-default" role="button">Cancel</a>'),
            Field(
                'next',
                css_class = 'hidden'
            ),
        )

class RegisterForm(Form):
    username = CharField(
        label = "Username",
        max_length = 100,
        required = True,
    )

    password = CharField(
        label = "Password",
        max_length = 100,
        required = True,
        widget = PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/charts/account/register/'
        self.helper.label_class = 'col-xs-12 col-md-1'
        self.helper.field_class = 'col-xs-12 col-md-5'
        self.helper.layout = Layout(
            'username',
            'password',
            StrictButton('Register', css_class='btn-primary col-md-offset-1', type='submit'),
            HTML('<a href="/charts/" class="btn btn-default" role="button">Cancel</a>')
        )