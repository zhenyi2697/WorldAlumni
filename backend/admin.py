from django.contrib import admin
from models import *

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sid', 'ref', 'ref_id' )

    def ref_id(self, obj):
        if obj.ref:
            return obj.ref.id
        else:
            return None

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'school', 'type', 'attend_year', 'finish_year')

class BindingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bind_from')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'gender', 'image_url')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'latitude', 'longitude', 'create_time', 'expire_time')

class SettingEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'binding', 'entry', 'value')

admin.site.register(School, SchoolAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Binding, BindingAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(SettingEntry, SettingEntryAdmin)
admin.site.register(UserSetting, UserSettingAdmin)
