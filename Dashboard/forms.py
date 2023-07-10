from django import forms
from .models import Notice_board

class NoticeboardForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Notice_board
        fields = '__all__'
        