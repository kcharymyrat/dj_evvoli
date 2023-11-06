from django import forms
from django.core.validators import EmailValidator, RegexValidator
from .models import Order


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class OrderForm(BootstrapFormMixin, forms.ModelForm):
    customer_name = forms.CharField(max_length=255, required=True)
    shipping_address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(
        validators=[RegexValidator(r"^\d{6}$")], required=True
    )  # regex for phone numbers
    email = forms.EmailField(
        validators=[EmailValidator()], required=False
    )  # email validation
    delivery_time = forms.DateTimeField(required=True)
    payment_option = forms.ChoiceField(
        choices=[
            ("", "Select Payment Option"),
            ("Cash", "Cash"),
            ("Card Terminal", "Card Terminal"),
        ],
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "shipping_address",
            "phone",
            "email",
            "delivery_time",
            "payment_option",
        ]
