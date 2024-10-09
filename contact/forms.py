from .models import Message
from django import forms
from .models import Reply

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']  # Only include the content field for the reply

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
