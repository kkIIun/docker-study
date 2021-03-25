from django.contrib import admin
from .models import Question, University, CustomUser
# Register your models here.
admin.site.register(Question)
admin.site.register(University)
admin.site.register(CustomUser)