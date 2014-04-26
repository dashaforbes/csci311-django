from django.db import models
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField
from crispy_forms.bootstrap import FormActions

# Create your models here.
class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.DateTimeField(auto_now=True)
    creator = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    
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

    assigned_to = models.CharField(max_length=100, blank=True)

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
    message_count = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.title)

class Component(models.Model):
    issue = models.ForeignKey(Issue)

    NONE = 'NA'
    TO3 = '2T'
    BENCHMARKS = 'BE'
    BUILD = 'BU'
    CTYPES = 'CT'
    DEMOS_TOOLS = 'DT'
    DEVGUIDE = 'DE'
    DISTUTILS = 'DI'
    DISTUTILS2 = 'D2'
    DOCUMENTATION = 'DO'
    EMAIL = 'EM'
    EXTENSION = 'EX'
    IDLE = 'ID'
    INSTALLATION = 'IN'
    INTERPRETER = 'IC'
    IO = 'IO'
    LIBRARY = 'LI'
    MACINTOSH = 'MA'
    REGEX = 'RE'
    TESTS = 'TE'
    TKINTER = 'TK'
    UNICODE = 'UN'
    WINDOWS = 'WI'
    XML = 'XM'
    COMPONENT_CHOICES = (
        (NONE, 'none'),
        (TO3, '2to3 (2.x to 3.0 conversion tool)'),
        (BENCHMARKS, 'Benchmarks'),
        (BUILD, 'Build'),
        (CTYPES, 'ctypes'),
        (DEMOS_TOOLS, 'Demos and Tools'),
        (DEVGUIDE, 'Devguide'),
        (DISTUTILS, 'Distutils'),
        (DISTUTILS2, 'Distutils2'),
        (DOCUMENTATION, 'Documentation'),
        (EMAIL, 'email'),
        (EXTENSION, 'Extension Modules'),
        (IDLE, 'IDLE'),
        (INSTALLATION, 'Installation'),
        (INTERPRETER, 'Interpreter Core'),
        (IO, 'IO'),
        (LIBRARY, 'Library (Lib)'),
        (MACINTOSH, 'Macintosh'),
        (REGEX, 'Regular Expressions'),
        (TESTS, 'Tests'),
        (TKINTER, 'Tkinter'),
        (UNICODE, 'Unicode'),
        (WINDOWS, 'Windows'),
        (XML, 'XML')
    )
    name = models.CharField(max_length=2, choices=COMPONENT_CHOICES, default=NONE)

    def __unicode__(self):
        return self.name

class Version(models.Model):
    issue = models.ForeignKey(Issue)
    version = models.CharField(max_length=10)

    def __unicode__(self):
        return self.version
    
class NosyList(models.Model):
    issue = models.ForeignKey(Issue)
    username = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username

class Commit(models.Model):
    hash = models.CharField(max_length=50,primary_key=True)
    author = models.CharField(max_length=100)
    time = models.DateTimeField('commit time')
    
    def __unicode__(self):
        return self.hash

class IssueForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'What\'s up',
                Div(
                    'title',
                    css_class = 'form-group'
                ),
                Div(
                    'assigned_to',
                    css_class = 'form-group'
                )
            ),
            Fieldset(
                'Bug Categories',
                Div(
                    'type',
                    css_class = 'form-group'
                ),
                Div(
                    'stage',
                    css_class = 'form-group'
                ),
                Div(
                    'priority',
                    css_class = 'form-group'
                ) 
            ),
            FormActions(
                Submit('submit', 'Add', css_class='button btn-primary')
            )
        )

    class Meta:
        model = Issue
        exclude = ('creator','message_count','status')

class ComponentForm(ModelForm):
    class Meta:
        model = Component
        exclude = ('issue',)

class VersionForm(ModelForm):
    class Meta:
        model = Version
        exclude = ('issue',)

class NosyListForm(ModelForm):
    class Meta:
        model = NosyList
        exclude = ('issue',)
