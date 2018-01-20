from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.models import User
from contacts.models import Contact, UserProfile
from contacts.forms import ContactForm, ImportContactsForm
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from .tables import ContactTable
from dateutil.relativedelta import relativedelta
from django.conf import settings
import mass_upload
import datetime
import itertools
import pytz
import logging
import traceback
import json
import os

logging.basicConfig(filename='test.log', level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s')

@login_required
def index(request):
    contacts_by_user_count = Contact.objects.filter(
                        added_by=request.user
                        ).count()

    total_contacts = Contact.objects.all().count()
    black_population = 89311
    percent_lf_added = format((total_contacts / 89311 * 100), '.2f')

    context = {
        # 'userprofile' : userprofile,
        'total_contacts' : total_contacts,
        'black_population' : black_population,
        'percent_lf_added' : percent_lf_added,
        'contacts_by_user_count': contacts_by_user_count
    }
    return render(request, 'contacts/index.html', context)

@login_required
def all_contacts(request):
    contacts = Contact.objects.all().order_by('-updated_at')
    count = contacts.count()

    date_string = datetime.datetime.now().strftime('%m%d%y')

    table = ContactTable(contacts)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('contacts_{0}.{1}'.format(date_string, export_format))

    context = {
        'contacts' : contacts,
        'count': count,
        'table': table
    }
    return render(request, 'contacts/all_contacts.html', context)

def my_contacts(request, username):
    if request.user.username != username:
        return redirect('index')
    contacts = Contact.objects.filter(
        added_by=request.user
    ).order_by('-updated_at')
    count = contacts.count()

    date_string = datetime.datetime.now().strftime('%m%d%y')

    table = ContactTable(contacts)
    table.exclude = ('added_by')
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('contacts_{0}.{1}'.format(date_string, export_format))

    context = {
        'contacts' : contacts,
        'count': count,
        'user' : request.user,
        'table': table
    }
    return render(request, 'contacts/my_contacts.html', context)

@login_required
def show_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.user != contact.added_by:
        return redirect('index')
    context = {'contact' : contact}
    return render(request, 'contacts/contact.html', context)

@login_required
def add_contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user:
                contact = form.save(commit=False)
                contact.added_by = request.user
                contact.save()
                return HttpResponseRedirect(reverse('contacts:show_contact', args=(contact.pk,)))
        else:
            print(form.errors)
    context = {'form' : form}
    return render(request, 'contacts/add_contact.html', context)

def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if contact.added_by != request.user:
        return redirect('index')
    form = ContactForm(instance=contact)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            if request.user:
                contact = form.save(commit=False)
                contact.added_by = request.user
                contact.save()
                return HttpResponseRedirect(reverse('contacts:show_contact', args=(contact.pk,)))
        else:
            print(form.errors)
    context = {
        'form' : form,
        'contact' : contact
    }
    return render(request, 'contacts/edit_contact.html', context)


def import_contacts(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('contacts:index'))
    form = ImportContactsForm()
    if request.method == 'POST':
        form = ImportContactsForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user:
                username = request.user.username
                fname = request.FILES['contact_file'].name
                size = request.FILES['contact_file'].size
                ext = os.path.splitext(request.FILES['contact_file'].name)[1]
                logging.debug(
                    '\n***import contacts file***\nuser: {0}\nfile: {1}\nsize: {2} bytes'.format(
                        username ,fname, size
                        )
                    )
                save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES['contact_file'].name)
                path = default_storage.save(save_path, request.FILES['contact_file'])
                print(path)
                try:
                    mass_upload.import_contacts(path, username)
                except:
                    logging.debug(
                        '\nImport Contacts Error: \n{}'.format(
                            traceback.format_exc()
                        )
                    )
                    return HttpResponseRedirect(reverse('contacts:import_failure'))
                else:
                    return HttpResponseRedirect(reverse('contacts:import_success'))
                finally:
                    default_storage.delete(path)
        else:
            print(form.errors)
    context = {'form' : form}
    return render(request, 'contacts/import_contacts.html', context)

@login_required
def import_success(request):
    tdelta = datetime.datetime.now(pytz.utc) - datetime.timedelta(seconds=7)
    contacts = Contact.objects.filter(
                updated_at__gte=tdelta
                ).filter(
                added_by=request.user
                ).order_by('-updated_at')
    count = contacts.count()

    date_string = datetime.datetime.now().strftime('%m%d%y')

    table = ContactTable(contacts)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(
            'recently_added_contacts_{0}.{1}'.format(date_string, export_format)
        )

    context = {
        'contacts' : contacts,
        'count': count,
        'user' : request.user,
        'table': table
    }
    if count == 0:
        return HttpResponseRedirect(reverse('contacts:index'))
    return render(request, 'contacts/import_success.html', context)

@login_required
def import_failure(request):
    return render(request, 'contacts/import_failure.html', {})

def search(request):
    result_list = []
    result_count = 0
    query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        print(query)
        if query:
            contacts_full_name = Contact.objects.filter(
                added_by=request.user
            ).filter(
                full_name__icontains=query
            ).order_by('-created_at')
            result_list = contacts_full_name
            result_count = result_list.count()
    context = {
        'result_list' : result_list,
        'result_count' : result_count,
        'query' : query
    }
    return render(request, 'contacts/search.html', context)


@api_view()
def user_activity(request):
    now = datetime.datetime.now(pytz.utc)
    tdelta = now - datetime.timedelta(weeks=12)
    contacts = Contact.objects.filter(
                        added_by=request.user
                        )
    if len(contacts) == 0:
        return Response({'no_activity': True})
    contacts_last_12_weeks = contacts.filter(
                            created_at__gte=tdelta
                            )

#***********************BY WEEK*************************************************

    grouped_by_week = itertools.groupby(
            contacts_last_12_weeks, lambda record: record.created_at.strftime("%W/%y")
            )
    contacts_by_week = [
        (week, len(list(contacts_this_week))) for week, contacts_this_week in grouped_by_week
        ]

    #get week strings for the last 12 weeks
    labels_weeks = []
    for i in range(12,-1,-1):
        labels_weeks.append(
            (now - datetime.timedelta(weeks=i)).strftime("%W/%y")
        )

    labels_week_of = []
    count_by_week = []
    for label in labels_weeks:
        week_of_string = (
                datetime.datetime.strptime(label + '-1', "%W/%y-%w")
            ).strftime("%m/%d/%y")
        try:
            count = [count for week, count in contacts_by_week if week == label][0]
        except IndexError:
            count = 0
        count_by_week.append({
            'week': week_of_string,
            'count': count
        })
        labels_week_of.append(week_of_string)
    count_by_week_data = [x['count'] for x in count_by_week]
#*********************************************************************************

#***********************BY MONTH*******************************************************

    grouped_by_month = itertools.groupby(
            contacts, lambda record: record.created_at.strftime("%m/%y")
            )
    contacts_by_month = [
        (month, len(list(contacts_this_month))) for month, contacts_this_month in grouped_by_month
        ]

    #get month labels
    first_month_string = '{}-01'.format(contacts_by_month[0][0])
    first_month_date = datetime.datetime.strptime(first_month_string, "%m/%y-%d")
    months_between = relativedelta(datetime.datetime.now(), first_month_date).months

    labels_months = []
    for i in range(months_between+1):
        labels_months.append(
            (first_month_date + relativedelta(months=+i)).strftime("%m/%y")
        )

    count_by_month = []
    for label in labels_months:
        try:
            count = [count for month, count in contacts_by_month if month == label][0]
        except IndexError:
            count = 0
        count_by_month.append({
                'month': label,
                'count': count
            })
    count_by_month_data = [x['count'] for x in count_by_month]
#*********************************************************************************

    data = {
        'by_week': {
            'labels': labels_week_of,
            'values': count_by_week_data
        },
        'by_month': {
            'labels': labels_months,
            'values': count_by_month_data
        },
    }

    return Response(data)
