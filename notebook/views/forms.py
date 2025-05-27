from django import forms
from django.core.exceptions import ValidationError
from notebook.models.models import Note, Notebook, Tag

class NoteForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Tags',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'séparés par des virgules',
            'class': 'tag-input-field'
        })
    )
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'notebook', 'is_favorite', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la note'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Écrivez votre note ici...'
            }),
            'notebook': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'is_favorite': 'Marquer comme favori',
            'is_pinned': 'Épingler cette note'
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        self.fields['notebook'].queryset = Notebook.objects.filter(user=user)
        
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(tag.name for tag in self.instance.tags.all())

    def clean_tags_input(self):
        """Valide et transforme la saisie des tags"""
        tags_str = self.cleaned_data.get('tags_input', '')
        tag_names = [name.strip() for name in tags_str.split(',') if name.strip()]
        
        # Limite le nombre de tags
        if len(tag_names) > 5:
            raise ValidationError("Maximum 5 tags autorisés.")
        
        return tag_names

    def save(self, commit=True):
        """Sauvegarde la note avec ses tags"""
        note = super().save(commit=False)
        
        if commit:
            note.save()
            self.save_m2m()
            
            tag_names = self.cleaned_data['tags_input']
            tags = []
            
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=name.lower(),
                    user=self.user,
                    defaults={'color': self._generate_tag_color()}
                )
                tags.append(tag)
            
            note.tags.set(tags)
        
        return note

    def _generate_tag_color(self):
        """Génère une couleur aléatoire pour les nouveaux tags"""
        import random
        colors = [
            '#6366f1', '#8b5cf6', '#ec4899', '#f97316', '#10b981',
            '#06b6d4', '#0ea5e9', '#a855f7', '#d946ef', '#f43f5e'
        ]
        return random.choice(colors)