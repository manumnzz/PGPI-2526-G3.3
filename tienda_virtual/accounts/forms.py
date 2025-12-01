from django import forms

from .models import CustomUser


class BaseRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    direccion = forms.CharField(label="Dirección", required=False)
    codigo_postal = forms.CharField(label="Código Postal", required=False)
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    telefono = forms.CharField(label="Teléfono", required=False)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "direccion",
            "codigo_postal",
            "fecha_nacimiento",
            "telefono",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "input-control", "placeholder": field.label}
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        return user


class UserRegisterForm(BaseRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = CustomUser.Roles.CLIENTE
        if commit:
            user.save()
        return user


class AdminRegisterForm(BaseRegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = CustomUser.Roles.ADMIN
        user.is_staff = True
        if commit:
            user.save()
        return user
