from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from contacts.models import Contact, UserProfile
from contacts.forms import ContactForm


from datetime import datetime

@login_required
def index(request):
    # contact_list = Contact.objects.order_by('-created_at')[:5]
    contact_list = Contact.objects.filter(
        added_by=request.user
    ).order_by('-created_at')[:5]
    context = {
        'contacts' : contact_list,
        'user' : request.user
    }
    return render(request, 'contacts/index.html', context)

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
