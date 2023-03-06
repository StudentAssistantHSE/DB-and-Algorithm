from django.contrib import admin
from .models import Account, Application, Project, ProjectTimetable, Status
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(admin.ModelAdmin):
    list_display = ("nickname", "email", 'name',)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("project", "getApplicant", 'message',)

    def getApplicant(self, obj):
        return obj.applicant.name
    getApplicant.short_description = 'Applicant name'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", 'getCreator',)

    def getCreator(self, obj):
        return obj.creator.name
    getCreator.short_description = 'Creator name'


class ProjectTimetableAdmin(admin.ModelAdmin):
    list_display = ("name", "getProject", 'deadline',)

    def getProject(self, obj):
        return obj.project.name
    getProject.short_description = 'Project name'


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTimetable, ProjectTimetableAdmin)
admin.site.register(Status)
