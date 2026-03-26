from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add tags separated by commas (e.g. python, django, web)'
        }),
        help_text="Separate tags with commas."
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover_image', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a compelling title...'
            }),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "-- Select Category --"
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Handle tags
            tags_input = self.cleaned_data.get('tags', '')
            tag_list = [t.strip() for t in tags_input.split(',') if t.strip()]
            instance.tags.set(*tag_list)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {'content': ''}


class PostFilterForm(forms.Form):
    author = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author username'})
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search posts...'})
    )
