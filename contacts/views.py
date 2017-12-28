from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.models import User
from contacts.models import Contact, UserProfile
from contacts.forms import ContactForm
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from .tables import ContactTable
import datetime
import itertools
import pytz
import logging
import json

# logging.basicConfig(filename='test.log', level=logging.DEBUG,
#     format='%(asctime)s:%(levelname)s:%(message)s')

@login_required
def index(request):
    userprofile = UserProfile.objects.get(user=request.user)

    now = datetime.datetime.now(pytz.utc)
    tdelta = now - datetime.timedelta(days=14)
    recently_added = Contact.objects.filter(
                        created_at__gte=tdelta
                        ).filter(
                        added_by=request.user
                        ).order_by('-created_at')

    total_contacts = Contact.objects.all().count()
    black_population = 89311
    percent_lf_added = format((total_contacts / 89311 * 100), '.3f')

    date_string = datetime.datetime.now().strftime('%m%d%y')

    table = ContactTable(recently_added)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('recent_contacts_{0}.{1}'.format(date_string, export_format))

    context = {
        'userprofile' : userprofile,
        'total_contacts' : total_contacts,
        'black_population' : black_population,
        'percent_lf_added' : percent_lf_added,
        'recently_added': recently_added,
        'table': table
    }
    return render(request, 'contacts/index.html', context)

@api_view()
def user_activity(request):
    now = datetime.datetime.now(pytz.utc)
    tdelta = now - datetime.timedelta(weeks=12)
    contacts = Contact.objects.filter(
                        added_by=request.user
                        )
    contacts_last_12_weeks = contacts.filter(
                            created_at__gte=tdelta
                            )

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

    grouped_by_month = itertools.groupby(
            contacts, lambda record: record.created_at.strftime("%m/%y")
            )
    contacts_by_month = [
        (day, len(list(contacts_this_month))) for day, contacts_this_month in grouped_by_month
        ]
    count_by_month = []
    for month, count in contacts_by_month:
        count_by_month.append({
            'month': month,
            'count': count
        })

    data = {
        'by_week': count_by_week,
        'by_month': count_by_month,
        'labels_week_of': labels_week_of
    }

    return Response(data)

def my_contacts(request, username):
    if request.user.username != username:
        return redirect('index')
    contacts = Contact.objects.filter(
        added_by=request.user
    ).order_by('-created_at')
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
        'user' : request.user,
        'table': table
    }
    return render(request, 'contacts/my_contacts.html', context)


#def recent_activity(request): #only for laborers

@login_required #only laborers can see
def history(request):
    contacts = Contact.objects.order_by('-updated_at')[:100]
    context = {
        'contacts' : contacts
    }
    return render(request, 'contacts/history.html', context)

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


# def stats(request):
