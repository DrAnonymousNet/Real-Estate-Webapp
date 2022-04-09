from django import forms

from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not have an account")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput)
    last_name = forms.CharField(required=True, max_length=30,
                                widget=forms.TextInput)
    email = forms.CharField(required=True, max_length=50,
                            widget=forms.EmailInput)

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        eqs = User.objects.filter(email=email)

        if eqs.count() != 0:
            raise forms.ValidationError("This Email already exist")
        if self.cleaned_data.get("password") != self.cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords must match !")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
