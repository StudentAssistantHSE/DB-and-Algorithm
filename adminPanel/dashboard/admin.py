from django.contrib import admin
from .models import Statuses, Faculties
from django.contrib.auth.admin import UserAdmin


class StatusesAdmin(admin.ModelAdmin):
    list_display = ["status"]

    def getStatus(self, obj):
        return obj.status.name
    getStatus.short_description = 'Status name'

class FacultyAdmin(admin.ModelAdmin):
    list_display = ["name", "shortname"]

    def getFaculty(self, obj):
        return obj.faculty.name
    getFaculty.short_description = 'Faculties'


# Register your models here.
# admin.site.register(Account, AccountAdmin)
admin.site.register(Statuses, StatusesAdmin)
admin.site.register(Faculties, FacultyAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(ProjectTimetable, ProjectTimetableAdmin)
# admin.site.register(Status)
