# interface/forms/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from core.models import Area, ConfiguracaoEstoque, Produto

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
            raise ValidationError('Por favor, informe um e-mail no formato correto.')
        domain = email.split('@')[1]
        if '.' not in domain:
            raise ValidationError('O domínio do e-mail deve conter um ponto (ex: .com, .br).')
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


class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
        help_text="Deixe em branco para não alterar a senha."
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
    )
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': 6,
        }),
        label="Áreas de Atuação"
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'papel',
            'matricula',
            'email',
            'areas',
            'ativo',
        ]
        field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'username'
            }),
            'papel': forms.Select(attrs={'class': 'form-select'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 or p2:
            if p1 != p2:
                self.add_error('password2', "As senhas não conferem.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get("password1")
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
            self.save_m2m()
        return user


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # inclui todos os campos, menos os gerados automaticamente
        fields = "__all__"
        exclude = [
            'quantidade_inicial',
            'criado_por',
            'criado_em',
        ]
        widgets = {
            'nfe_numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da NFe'
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escaneie ou digite o código'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do produto'
            }),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'lote': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'id': 'id_lote'
            }),
            'validade': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'preco_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nfe_numero': 'NFe Nº',
            'codigo_barras': 'Código de Barras',
            'descricao': 'Descrição',
            'fornecedor': 'Fornecedor',
            'area': 'Área',
            'lote': 'Lote',
            'validade': 'Validade',
            'quantidade': 'Quantidade Atual',
            'preco_unitario': 'Preço Unitário',
            'status': 'Status',
        }
