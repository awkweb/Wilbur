from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, SetPasswordForm
from django.contrib.auth import password_validation

from cuser.models import CUser


class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'placeholder': 'charlotte@web.net',
            'class': 'form-control large',
            'spellcheck': 'false',
            'autofocus': ''
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Super, secret',
            'class': 'form-control large'
        })


class UserBetaCreationForm(forms.ModelForm):
    error_messages = {
        'code_mismatch': "The code didn't match.",
    }
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'placeholder': 'charlotte@web.net',
            'class': 'form-control large', 'required': 'required', 'spellcheck': 'false', 'autofocus': ''})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Super, secret',
                                          'class': 'form-control large', 'required': 'required'}),
    )
    code = forms.CharField(
        label="Code",
        widget=forms.PasswordInput(attrs={'placeholder': 'Your ticket to the party',
                                          'class': 'form-control large', 'required': 'required'}),
    )

    class Meta:
        model = CUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserBetaCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': ''})

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if code != 'ebwhite':
            raise forms.ValidationError(
                self.error_messages['code_mismatch'],
                code='code_mismatch',
            )
        self.instance.email = self.cleaned_data.get('email')
        return code

    def save(self, commit=True):
        user = super(UserBetaCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'placeholder': 'charlotte@web.net',
            'class': 'form-control large', 'required': 'required', 'autofocus': 'autofocus'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Super, secret',
                                          'class': 'form-control large', 'required': 'required'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'You know the drill',
                                          'class': 'form-control large', 'required': 'required'}),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = CUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': ''})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.email = self.cleaned_data.get('email')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text="Raw passwords are not stored, so there is no way to see "
                                                   "this user's password, but you can change the password "
                                                   "using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = CUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=255,
        widget=forms.EmailInput(attrs={
            'placeholder': 'charlotte@web.net',
            'class': 'form-control', 'required': 'required'})
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.B.', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'White', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UserProfileForm, self).__init__(*args, **kwargs)


class EditPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Super, secret', 'class': 'form-control', 'autofocus': ''
        })
        self.fields['new_password2'].label = 'Confirm New Password'
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'placeholder': 'You know the drill.', 'class': 'form-control'
        })
