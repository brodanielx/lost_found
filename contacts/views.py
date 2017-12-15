from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from contacts.models import Contact, UserProfile
from contacts.forms import ContactForm
import datetime
import pytz
import logging

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
                        ).order_by('-created_at')[:5]

    # active_users = [recent_contacts_list[0].added_by]
    # for i in range(1, len(recent_contacts_list)):
    #     if recent_contacts_list[i].added_by != recent_contacts_list[i-1].added_by:
    #         active_users.append(recent_contacts_list[i].added_by)
    #
    # recently_added_counts = []
    # for user in active_users:
    #     recently_added_count = recent_contacts_list.filter(
    #                                     added_by=user).count()
    #     recently_added_counts.append({
    #         'user': user,
    #         'count': recently_added_count
    #     })

    total_contacts = Contact.objects.all().count()
    black_population = 89311
    percent_lf_added = format((total_contacts / 89311 * 100), '.3f')

    context = {
        'userprofile' : userprofile,
        'total_contacts' : total_contacts,
        'black_population' : black_population,
        'percent_lf_added' : percent_lf_added,
        'recently_added': recently_added
    }
    return render(request, 'contacts/index.html', context)

def my_contacts(request, username):
    #make grid sortable
    if request.user.username != username:
        return redirect('index')
    contacts = Contact.objects.filter(
        added_by=request.user
    ).order_by('-created_at')
    count = contacts.count()
    context = {
        'contacts' : contacts,
        'count': count,
        'user' : request.user
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
def my_profile(request, username):
    if request.user.username != username:
        return redirect('index')
    contact_list = Contact.objects.filter(
        added_by=request.user
    ).order_by('-created_at')[:5]
    context = {
        'contacts' : contact_list,
        'user' : request.user
    }
    return render(request, 'contacts/my_profile.html', context)

@login_required
def show_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
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


# def stats(request):
