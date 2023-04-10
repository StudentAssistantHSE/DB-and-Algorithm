from django.contrib import admin
from .models import Statuses, Faculties, Applications, Categories, \
    ProjectCategories, Projects, ProjectsTimetable, UserCategories, UserRecommendations, Users
from django.contrib.auth.admin import UserAdmin


class StatusesAdmin(admin.ModelAdmin):
    list_display = ["status"]
    search_fields = ('status',)

    def getStatus(self, obj):
        return obj.status.name

    getStatus.short_description = 'Status name'


class FacultyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "shortname"]
    search_fields = ('name', 'shortname')

    def getFaculty(self, obj):
        return obj.faculty.name

    getFaculty.short_description = 'Faculties'


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["project", "applicant", "created_date", "message", "status"]
    search_fields = ("project__name", "applicant__fullname", "status__status")
    list_filter = ["status"]

    def getAppliсation(self, obj):
        return obj.project.name

    getAppliсation.short_description = 'Заявки на проекты'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "is_custom"]
    search_fields = ("category", )
    list_filter = ["is_custom"]
    def getCategory(self, obj):
        return obj.category.name

    getCategory.short_description = 'Теги'


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ("name", )

    def getProjects(self, obj):
        return obj.project.name

    getProjects.short_description = 'Проекты'

class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["project", "category"]
    search_fields = ("project__name", "category__category")

class ProjectTimetableAdmin(admin.ModelAdmin):
    list_display = ["project", "deadline", "name", "description"]
    search_fields = ("project__name", "name")

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ["user", "category"]
    search_fields = ("user__fullname", "category__category")

class UserRecommendationsAdmin(admin.ModelAdmin):
    list_display = ["user", "project", "generated_date"]
    search_fields = ("user__fullname", "project__name")
    list_filter = ["generated_date"]

class UsersAdmin(admin.ModelAdmin):
    list_display = ["email", "fullname", "last_login", "description", "bio", "faculty", "password", "created_date", "updated_date"]
    search_fields = ("email", "fullname", "faculty__name")
    list_filter = ["faculty", "created_date"]



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
