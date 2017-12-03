from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from contacts.models import Contact, UserProfile
from django.contrib.auth.models import User
# from links.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    contact_list = Contact.objects.order_by('-created_at')[:5]
    context = {
        'contacts' : contact_list
    }
    return render(request, 'contacts/index.html', context)

def show_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    context = {'contact' : contact}
    return render(request, 'contacts/contact.html', context)
