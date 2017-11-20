from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from links.models import Category, Page, UserProfile
from django.contrib.auth.models import User
# from links.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    context = {
        'test' : 'this is a test'
    }
    return render(request, 'contacts/index.html', context)
