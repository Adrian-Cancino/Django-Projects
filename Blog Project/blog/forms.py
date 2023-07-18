from django.forms import ModelForm, TextInput

from .models import Comments

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'body']
        widgets = {
            'name': TextInput(attrs={'class': 'input'}),
            'email': TextInput(attrs= {'class': 'input'}),
            'body': TextInput(attrs = {'class': 'textarea'})
        }