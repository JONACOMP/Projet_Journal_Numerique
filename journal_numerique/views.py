from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Count

from django.utils import timezone
from datetime import timedelta

from notebook.models.models import *

class Home(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "index.html"

    def get(self, request, *args, **kwargs):

        context = {
            'user': request.user,
            'note_count': Note.objects.filter(user=request.user).count(),
            'tag_count': Tag.objects.filter(user=request.user).count(),
            'favorite_notes': Note.objects.filter(user=request.user, is_favorite=True).count(),
            'recent_activity': Note.objects.filter(user=request.user, updated_at__gte=timezone.now()-timedelta(days=30)).count(),
            'recent_notes': Note.objects.filter(user=request.user).order_by('-updated_at')[:6],
            'frequent_tags': Tag.objects.filter(user=request.user).annotate(count=Count('notes')).order_by('-count')[:10],
            'notebooks': Notebook.objects.filter(user=request.user)
        }
        return render(request,self.template_name,context)
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            title = request.POST.get("title")
            if title:
                Notebook.objects.create(user=request.user, title=title)
        context = {
            'user': request.user,
            'note_count': Note.objects.filter(user=request.user).count(),
            'tag_count': Tag.objects.filter(user=request.user).count(),
            'favorite_notes': Note.objects.filter(user=request.user, is_favorite=True).count(),
            'recent_activity': Note.objects.filter(user=request.user, updated_at__gte=timezone.now()-timedelta(days=30)).count(),
            'recent_notes': Note.objects.filter(user=request.user).order_by('-updated_at')[:6],
            'frequent_tags': Tag.objects.filter(user=request.user).annotate(count=Count('notes')).order_by('-count')[:10],
            'notebooks': Notebook.objects.filter(user=request.user)
        }
        return render(request,self.template_name,context)

    
    