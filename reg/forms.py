from django import forms
from .models import User

class RegForm(forms.Form):
    email = forms.EmailField(label="E-mail адрес", error_messages={'invalid':"Некорректный e-mail"})
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Подтвердите пароль")
    real_name = forms.CharField(label="Ваше имя")
    bio = forms.CharField(widget=forms.Textarea, label="Пару слов о себе")
    CHOICES = (('1', 'First',), ('2', 'Second',))
    # is_customer = forms.BooleanField(widget=forms.RadioSelect, choices = CHOICES)


    def clean(self):
        cleaned_data = super(RegForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        errmsg = []

        if(User.objects.filter(username=cleaned_data.get("email"))):
            errmsg.append("Пользователь с таким e-mail уже есть")

        if password != confirm_password:
            errmsg.append("Пароли не совпадают")

        if len(password) < 8:
            errmsg.append("Пароль должен быть не короче 8 символов")

        if errmsg != []:
            if "Пользователь с таким e-mail уже есть" in errmsg:
                super(RegForm, self).add_error('email', errmsg[0])
                errmsg.pop(0)
            super(RegForm, self).add_error('password', ", ".join(errmsg))
            super(RegForm, self).add_error('confirm_password', "")

class LoginForm(forms.Form):
    name = forms.EmailField(label="E-mail адрес", error_messages={'invalid': "Некорректный e-mail"})
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")


class ViewForm(object):
    pass