from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post,Category,Tag
from django.contrib.auth.models  import User

class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)


class PostAddForm(forms.Form):
    desc = forms.CharField(widget=forms.TextInput, label='摘要', required=True)
    content = forms.CharField(widget=forms.Textarea, label='正文', required=True)
    title = forms.CharField(widget=forms.TextInput, label='标题', required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.filter(status=Category.STATUS_NORMAL),label='分类',required=True)
    owner = forms.ModelChoiceField(queryset=User.objects.all(),label='作者')