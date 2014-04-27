from django.contrib import admin
from charts.models import Issue, Component, Version, People, Developer, Commit

# Register your models here.
admin.site.register(Issue)
admin.site.register(Component)
admin.site.register(Version)
admin.site.register(People)
admin.site.register(Developer)
admin.site.register(Commit)
