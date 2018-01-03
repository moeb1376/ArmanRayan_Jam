from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([University, Competition, Language, Grade])
