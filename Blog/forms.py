from django import forms
from database.models import Blogs, Categories
from django_quill.forms import QuillFormField

class BlogPostForm(forms.ModelForm):
    content = QuillFormField()
    
    class Meta:
        model = Blogs
        fields = ['title', 'content', 'blog_img', 'categories', 'status']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'blog_img': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['content'].required = True
        self.fields['blog_img'].required = True
        self.fields['categories'].required = True
        self.fields['status'].required = True
        
        # Update categories choices with a default option
        self.fields['categories'].widget.choices = [('', 'Select a category')] + [
            (category.id, category.name) for category in Categories.objects.all()
        ]
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError("Content must be at least 50 characters long.")
        return content