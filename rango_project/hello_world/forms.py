from django import forms
from hello_world.models import category,Page,UserProfile
from django.contrib.auth.models import User



class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Enter Category")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget = forms.HiddenInput(), initial=0)

    class Meta:
        model = category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Enter Title")
    url = forms.URLField(max_length=200,help_text="Enter the URL of the page")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('cat',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('https://'):
            url = 'https://' + url
            cleaned_data['url'] = url
        return cleaned_data



class UserForm(forms.ModelForm):
    # username = forms.CharField(max_length=128,help_text="Enter Title")
    # email = forms.EmailField(max_length=128,help_text="Enter Title")
    # password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False) 
    picture = forms.ImageField(required=False)


    class Meta:
        model = UserProfile
        exclude = ('user',)

class EditCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Enter Category")

    class Meta:
        model = category
        fields = ('name',)