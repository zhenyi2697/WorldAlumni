from django.contrib import admin
from models import *

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sid')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'school', 'type', 'attend_year', 'finish_year')

class BindingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bind_from')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'gender', 'image_url')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'latitude', 'longitude')

admin.site.register(School, SchoolAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Binding, BindingAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)
