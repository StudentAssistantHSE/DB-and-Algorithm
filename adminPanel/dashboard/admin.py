from django.contrib import admin
from .models import Statuses, Faculties, Applications
from django.contrib.auth.admin import UserAdmin


class StatusesAdmin(admin.ModelAdmin):
    list_display = ["status"]

    def getStatus(self, obj):
        return obj.status.name
    getStatus.short_description = 'Status name'

class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "shortname"]

    def getFaculty(self, obj):
        return obj.faculty.name
    getFaculty.short_description = 'Faculties'

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["project", "applicant", "created_date", "message", "status"]

    def getAppliсation(self, obj):
        return obj.project.name
    getAppliсation.short_description = 'Заявки на проекты'


# Register your models here.
# admin.site.register(Account, AccountAdmin)
admin.site.register(Statuses, StatusesAdmin)
admin.site.register(Faculties, FacultyAdmin)
admin.site.register(Applications, ApplicationAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(ProjectTimetable, ProjectTimetableAdmin)
# admin.site.register(Status)
