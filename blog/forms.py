from django import forms
from .models import Comment

#here form you have created of your own
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

#here we are using model based
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')

class SearchForm(forms.Form):
    query=forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(LoginForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user