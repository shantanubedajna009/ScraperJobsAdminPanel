from django import forms
from rss_app.models import Added_Jobs
from django import forms
from django.contrib.auth.models import User
from rss_app.models import UserInfo

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserInfoForm(forms.ModelForm):

    class Meta():
        model = UserInfo
        fields = ('website', 'picture')

class JobForm(forms.ModelForm):

    class Meta():
        model = Added_Jobs
        fields = ('date_created', 'name', 'link')

        widgets = {
            'date_created': forms.HiddenInput(),
        }

        def name(self):

            name=self.cleaned_data.get('name')
            if len(name) <= 2:
                raise forms.ValidationError("name cannot be empty")
            return name

        def clean_link(self):

            link=self.cleaned_data.get('link')
            if len(link) <= 2:
                raise forms.ValidationError("link cannot be empty")
            return link
