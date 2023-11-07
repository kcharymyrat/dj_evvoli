from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import Order


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control mb-2"})


class OrderForm(BootstrapFormMixin, forms.ModelForm):
    customer_name = forms.CharField(label="", max_length=255, required=True)
    shipping_address = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
            }
        ),
        required=True,
    )
    phone = forms.CharField(
        label="",
        validators=[RegexValidator(r"^\d{8}$")],
        help_text=_("Provide only 8 digits, don't start with +993 or 8 6x"),
        required=True,
    )
    email = forms.EmailField(label="", validators=[EmailValidator()], required=False)
    delivery_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
                "required": "True",
            }
        ),
        label="Delivery Time",
    )
    payment_option = forms.ChoiceField(
        choices=[
            ("Cash", "Cash"),
            ("Card Terminal", "Card Terminal"),
        ],
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "phone",
            "email",
            "shipping_address",
            "delivery_time",
            "payment_option",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer_name"].widget.attrs.update(
            {"placeholder": _("Full Name")}
        )
        self.fields["phone"].widget.attrs.update({"placeholder": _("Phone")})
        self.fields["email"].widget.attrs.update({"placeholder": _("E-mail")})
        self.fields["shipping_address"].widget.attrs.update(
            {"placeholder": _("Address")}
        )
        self.fields["payment_option"].widget.attrs.update(
            {"placeholder": _("Select Payment Option")}
        )
