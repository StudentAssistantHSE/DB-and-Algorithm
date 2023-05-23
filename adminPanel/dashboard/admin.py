from django.contrib import admin
from django.http import HttpResponse
import csv, datetime
from django.db import models
import openpyxl
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .models import Statuses, Faculties, Applications, Categories, \
    ProjectCategories, Projects, ProjectsTimetable, UserCategories, UserRecommendations, Users, Role, UsersRoles


@admin.action(description="Скачать в Эксель")
def export_to_excel(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.xlsx'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write header row
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    header_row = [field.verbose_name for field in fields if hasattr(field, 'verbose_name')]
    worksheet.append(header_row)

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            if hasattr(field, 'verbose_name'):
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                elif isinstance(value, models.Model):
                    value = str(value)
                data_row.append(value)
        worksheet.append(data_row)

    workbook.save(response)
    return response



class StatusesAdmin(admin.ModelAdmin):
    list_display = ["status"]
    search_fields = ('status',)
    actions = [export_to_excel]

    def getStatus(self, obj):
        return obj.status.name

    getStatus.short_description = 'Status name'


class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "shortname"]
    search_fields = ('name', 'shortname')
    actions = [export_to_excel]

    def getFaculty(self, obj):
        return obj.faculty.name

    getFaculty.short_description = 'Faculties'


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["project", "applicant", "created_date", "message", "status"]
    search_fields = ("project__name", "applicant__fullname", "status__status")
    list_filter = ["status"]
    actions = [export_to_excel]

    def getAppliсation(self, obj):
        return obj.project.name

    getAppliсation.short_description = 'Заявки на проекты'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "is_custom"]
    search_fields = ("category", )
    list_filter = ["is_custom"]
    actions = [export_to_excel]
    def getCategory(self, obj):
        return obj.category.name

    getCategory.short_description = 'Теги'


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ("name", )
    actions = [export_to_excel]

    def getProjects(self, obj):
        return obj.project.name

    getProjects.short_description = 'Проекты'

class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["project", "category"]
    search_fields = ("project__name", "category__category")
    actions = [export_to_excel]

class ProjectTimetableAdmin(admin.ModelAdmin):
    list_display = ["project", "deadline", "name", "description"]
    search_fields = ("project__name", "name")
    actions = [export_to_excel]

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ["user", "category"]
    search_fields = ("user__fullname", "category__category")
    actions = [export_to_excel]

class UserRecommendationsAdmin(admin.ModelAdmin):
    list_display = ["user", "project", "generated_date"]
    search_fields = ("user__fullname", "project__name")
    list_filter = ["generated_date"]
    actions = [export_to_excel]

class UsersAdmin(admin.ModelAdmin):
    list_display = ["email", "fullname", "last_login", "description", "bio", "faculty", "password", "created_date", "updated_date"]
    search_fields = ("email", "fullname", "faculty__name")
    list_filter = ["faculty", "created_date"]
    actions = [export_to_excel]



# Register your models here.
# admin.site.register(Account, AccountAdmin)
admin.site.register(Statuses, StatusesAdmin)
admin.site.register(Faculties, FacultyAdmin)
admin.site.register(Applications, ApplicationAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(ProjectCategories, ProjectCategoryAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(ProjectsTimetable, ProjectTimetableAdmin)
admin.site.register(UserCategories, UserCategoryAdmin)
admin.site.register(UserRecommendations, UserRecommendationsAdmin)
admin.site.register(Users, UsersAdmin)

