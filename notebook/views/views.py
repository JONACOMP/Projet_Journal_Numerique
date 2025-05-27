from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

from .forms import NoteForm
from notebook.models import Notebook, Note

from . import permissions

class NewNoteView(LoginRequiredMixin, View):
    template_name = 'notebook/newnote.html' 
    
    def get(self, request, *args, **kwargs):
        form = NoteForm(user=request.user)
        context = {
            'notebooks': Notebook.objects.filter(user=request.user),
            'form': form,
            'page_title': 'Nouvelle Note'
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST, request.FILES, user=request.user)
    
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            form.save_m2m()
            return redirect('notebook:detail', pk=note.pk)
        
        context = {
            'notebooks': Notebook.objects.filter(user=request.user),
            'form': form,
            'page_title': 'Nouvelle Note'
        }
        return render(request, self.template_name, context)
    
    
class NoteDetailView(LoginRequiredMixin, permissions.IsOwnerOrSharedReadOnly, DetailView):
    model = Note
    template_name = 'notebook/detail.html'
    context_object_name = 'note'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        """Ne montre que les notes de l'utilisateur ou partagées avec lui"""
        return Note.objects.filter(
            Q(user=self.request.user) |
            Q(shares__user=self.request.user)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ajout des données supplémentaires
        context['page_title'] = self.object.title
        context['versions'] = self.object.versions.order_by('-created_at')[:5]
        context['can_edit'] = self.request.user == self.object.user
        
        return context    


def notebook_delete(request, pk):
    if request.method == "POST":
        notebook = get_object_or_404(Notebook, pk=pk)
        notebook.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def note_delete(request, pk):
    if request.method == "POST":
        note = get_object_or_404(Note, pk=pk)
        note.delete()
    return redirect('/')