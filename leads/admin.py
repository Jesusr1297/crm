from django.contrib import admin
from leads import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Agent)
admin.site.register(models.Lead)
admin.site.register(models.UserProfile)
admin.site.register(models.Category)
