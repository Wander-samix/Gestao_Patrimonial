from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from core.models import Area, ConfiguracaoEstoque, Produto
# Substituímos o import direto de Usuario pelo get_user_model()
Usuario = get_user_model()


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da Área'
            }),
        }


class ConfiguracaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoEstoque
        fields = ['area', 'estoque_minimo']
        widgets = {
            'area': forms.Select(attrs={'class': 'form-select'}),
            'estoque_minimo': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 100
            }),
        }
        labels = {
            'area': 'Área',
            'estoque_minimo': 'Estoque mínimo (%)',
        }


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@dominio.com',
            'autocomplete': 'email'
        }),
        error_messages={'invalid': 'Insira um e-mail válido.'}
    )

    password1 = forms.CharField(
        label="Nova senha",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nova senha',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label="Confirme a nova senha",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email']
        field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autocomplete': 'username'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(
                'Por favor, informe um e-mail no formato correto.'
            )
        domain = email.split('@')[1]
        if '.' not in domain:
            raise ValidationError(
                'O domínio do e-mail deve conter um ponto (ex: .com, .br).'
            )
        return email.lower()

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 or p2:
            if p1 != p2:
                self.add_error('password2', "As senhas não conferem.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        nova = self.cleaned_data.get("password1")
        if nova:
            user.set_password(nova)
        if commit:
            user.save()
        return user


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # inclui TODOS os campos do model...
        fields = "__all__"
        # ...menos estes
        exclude = [
            'lote',
            'quantidade_inicial',
            'criado_por',
            'criado_em',
        ]
        widgets = {
            'nfe_numero':     forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras':  forms.TextInput(attrs={'class': 'form-control'}),
            'descricao':      forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor':     forms.Select   (attrs={'class': 'form-select'}),
            'area':           forms.Select   (attrs={'class': 'form-select'}),
            'validade':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade':     forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status':         forms.Select   (attrs={'class': 'form-select'}),
        }


# Alias para o controller que importa UsuarioForm
UsuarioForm = ProfileForm
