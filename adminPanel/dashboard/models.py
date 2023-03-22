# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Applications(models.Model):
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    applicant = models.ForeignKey('Users', models.DO_NOTHING)
    created_date = models.DateField()
    message = models.TextField()
    status = models.ForeignKey('Statuses', models.DO_NOTHING, db_column='status', blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        managed = False
        db_table = 'applications'
        unique_together = (('id', 'project', 'applicant'),)

    def __str__(self):
        return self.project.name


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Categories(models.Model):
    category = models.TextField(unique=True)
    is_custom = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        managed = False
        db_table = 'categories'

    def __str__(self):
        return self.category


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Faculties(models.Model):
    name = models.TextField()
    shortname = models.TextField()

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
        managed = False
        db_table = 'faculties'

    def __str__(self):
        return self.name



class Projects(models.Model):
    name = models.TextField()
    description = models.TextField()
    contacts = models.TextField(blank=True, null=True)
    created_date = models.DateField()
    updated_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    creator_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    is_closed = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        managed = False
        db_table = 'projects'

    def __str__(self):
        return self.name

class ProjectCategories(models.Model):
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    category = models.ForeignKey(Categories, models.DO_NOTHING)

    class Meta:
        verbose_name = 'Теги проекта'
        verbose_name_plural = 'Теги проектов'
        managed = False
        db_table = 'project_categories'
        unique_together = (('project', 'category'),)

    def __str__(self):
        return self.project.name


class ProjectsTimetable(models.Model):
    project = models.ForeignKey(Projects, models.DO_NOTHING, blank=True, null=True)
    deadline = models.DateField()
    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Дедлайн'
        verbose_name_plural = 'Дедлайны'
        managed = False
        db_table = 'projects_timetable'

    def __str__(self):
        return str(self.project.name + " " + self.name.name)


class Statuses(models.Model):
    status = models.TextField(unique=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        managed = False
        db_table = 'statuses'

    def __str__(self):
        return self.status.name


class UserCategories(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING)

    class Meta:
        verbose_name = 'Теги пользователя'
        verbose_name_plural = 'Теги пользователей'
        managed = False
        db_table = 'user_categories'
        unique_together = (('user', 'category'),)

    def __str__(self):
        return str(self.user.name + " " + self.category)


class UserRecommendations(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    project = models.ForeignKey(Projects, models.DO_NOTHING)
    generated_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Рекомендации пользователю'
        verbose_name_plural = 'Рекомендации пользователям'
        managed = False
        db_table = 'user_recommendations'


class Users(models.Model):
    email = models.TextField(unique=True)
    fullname = models.TextField()
    last_login = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    faculty = models.ForeignKey(Faculties, models.DO_NOTHING, blank=True, null=True)
    password = models.TextField()
    created_date = models.DateField()
    updated_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.fullname
