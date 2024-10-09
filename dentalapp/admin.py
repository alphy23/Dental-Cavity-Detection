from django.contrib import admin

# Register your models here.
from . models import reg,normal,xray

admin.site.register(reg)
admin.site.register(normal)
admin.site.register(xray)