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
    recent_contacts_list = Contact.objects.filter(
                        created_at__gte=tdelta
                        ).order_by('-created_at')

    active_users = [recent_contacts_list[0].added_by]
    for i in range(1, len(recent_contacts_list)):
        if recent_contacts_list[i].added_by != recent_contacts_list[i-1].added_by:
            active_users.append(recent_contacts_list[i].added_by)

    recently_added_counts = []
    for user in active_users:
        recently_added_count = recent_contacts_list.filter(
                                        added_by=user).count()
        recently_added_counts.append({
            'user': user,
            'count': recently_added_count
        })

    context = {
        'userprofile' : userprofile,
        'recently_added_counts' : recently_added_counts,
        'now' : now,
        'tdelta' : tdelta
    }
    return render(request, 'contacts/index.html', context)

# def timeline(request):


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

# def stats(request):
