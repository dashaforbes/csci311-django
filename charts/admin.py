from django.contrib import admin
from charts.models import Issues, Component, Version, NosyList, Commit

# Register your models here.
admin.site.register(Issues)
admin.site.register(Component)
admin.site.register(Version)
admin.site.register(NosyList)
admin.site.register(Commit)
