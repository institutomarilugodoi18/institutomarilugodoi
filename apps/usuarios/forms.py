from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UsuarioCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_staff',
            'is_active',
        ]
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Primeiro nome',
            'last_name': 'Sobrenome',
            'is_staff': 'Usuário da equipe',
            'is_active': 'Usuário ativo',
        }
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este e-mail.')

        return email


class UsuarioUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='E-mail'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
        ]
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Primeiro nome',
            'last_name': 'Sobrenome',
            'is_staff': 'Usuário da equipe',
            'is_active': 'Usuário ativo',
        }
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este e-mail.')

        return email