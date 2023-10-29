from django.forms import ModelForm
from django import forms
from .models import Post, AdvUser, user_registrated, Comment, Consult, Vist, Event
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class Index(forms.Form):
    Начало = forms.DateTimeField(widget=forms.SelectDateWidget)
    Конец = forms.DateTimeField(widget=forms.SelectDateWidget)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'post': forms.HiddenInput, 'author': forms.HiddenInput,'moderation':forms.HiddenInput,'vist': forms.HiddenInput}


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = AdvUser
        fields = ('username', 'avatar', 'email', 'first_name', 'last_name','phone_num','faculty','group')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password(repeat)', widget=forms.PasswordInput,
                                help_text='Repeat password')

    def clean_passwird1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Passwords do not match',
                                                   code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'avatar', 'email', 'password1', 'password2',
                  'first_name', 'last_name','phone_num','faculty','group')

class Subscribe(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    pass

class Subscribeg(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    colvo = forms.IntegerField(min_value=1)

class UnSubscribeg(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    colvo = forms.IntegerField(min_value=1)

class Subscribegv(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class NewConsult(ModelForm):
    eventdate = forms.DateTimeField(widget=forms.SelectDateWidget,label='Дата')
    class Meta:
        model = Consult
        fields = '__all__'
        widgets = {'zan': forms.HiddenInput}

class zapis_consult(forms.Form):
    pass

class PostForm(ModelForm):
    eventdate = forms.DateTimeField(widget=forms.SelectDateWidget,label='Дата')
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {'author': forms.HiddenInput, 'zapis':forms.HiddenInput,'mesta_now':forms.HiddenInput}

class TvorForm(forms.Form):
    Роль = forms.ChoiceField(choices=(("Артист", "Артист"), ("Организатор", "Организатор")))

class VistForm(ModelForm):
    class Meta:
        model = Vist
        fields = '__all__'
        widgets = {'author': forms.HiddenInput,'event': forms.HiddenInput}
