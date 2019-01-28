from django.contrib import admin
from hello_world.models import category,Page
from hello_world.models import student,UserProfile
from django.contrib.auth.models import User
# Register your models here.


class AdminPage(admin.ModelAdmin):
    list_display = ('cat','title','url')

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(category,categoryAdmin)
admin.site.register(Page,AdminPage)
admin.site.register(student)
admin.site.register(UserProfile)