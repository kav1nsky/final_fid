from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User



class AgreementForm(forms.Form):
    acceptor_email = forms.EmailField(label="E-mail адрес акцептанта", error_messages={'invalid':"Некорректный e-mail"})
    content = forms.CharField(widget=forms.Textarea, label="Текст соглашения")
    timestamp = forms.DateTimeField(widget=forms.DateTimeInput, label="Дата и время завершения контракта")

    def clean(self):
        cleaned_data = super(AgreementForm, self).clean()
        errmsg = []

        if not User.objects.filter(username=cleaned_data.get("email")):
            errmsg.append("Пользователь с таким e-mail не найден")


        if errmsg != []:
                super(AgreementForm, self).add_error('email', errmsg[0])