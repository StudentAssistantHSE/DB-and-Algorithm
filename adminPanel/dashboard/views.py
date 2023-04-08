from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.mail import send_mass_mail
from django.conf import settings
from django.utils.text import camel_case_to_spaces

from adminPanel.dashboard.models import Users, Faculties


# Create your views here.
def index(request):
    return render(request, 'admin/index.html')


@login_required
def email(request):
    app_list = []

    for app_config in apps.get_app_configs():
        models = app_config.get_models()
        if models:
            app_name = camel_case_to_spaces(app_config.name.split('.')[-1])
            app_list.append({
                'name': app_name.capitalize() + 's',
                'models': models,
            })
    print(len(app_list))
    emails = Users.objects.all()
    faculties = Faculties.objects.all()
    faculties_emails = {}
    for faculty in faculties:
        test = Users.objects.filter(faculty__name=faculty).values_list('email', flat=True)
        faculties_emails[faculty.name] = test
    context = {'app_list': app_list, 'emails': emails, 'faculties': faculties, 'faculty_email': faculties_emails}
    return render(request, 'admin/email.html', context)


def send_mails(request):
    emails = Users.objects.all()
    faculties = Faculties.objects.all()
    faculties_emails = {}
    for faculty in faculties:
        test = Users.objects.filter(faculty__name=faculty).values_list('email', flat=True)
        faculties_emails[faculty.name] = test
    context = {'emails': emails, 'faculties': faculties, 'faculty_email': faculties_emails}
    if request.method == 'POST':
        email_address = request.POST.get('email')
        emails = email_address.split('; ')
        send_to = []
        for em in emails:
            if em in faculties_emails:
                send_to += faculties_emails[em]
            else:
                send_to.append(em)
        topic = request.POST.get('topic')
        text = request.POST.get('text')
        print((send_to))
        data = {'email': send_to, 'topic': topic, 'text': text}
        try:
            message_tuple = (data['topic'], data['text'], settings.EMAIL_HOST_USER, send_to)
            res = send_mass_mail([message_tuple])
            return JsonResponse({'message': 'Form submitted successfully!'})
        except Exception as e:
            return JsonResponse({'message': 'Form submitted unsuccessfully!'})
