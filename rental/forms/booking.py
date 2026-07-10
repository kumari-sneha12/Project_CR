from django import forms
from datetime import date
from rental.models.booking import Booking, Payment

class BookingForm(forms.ModelForm):
    pickup_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date', 'min': date.today().strftime('%Y-%m-%d'), 'id': 'id_pickup_date'
    }))
    return_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date', 'min': date.today().strftime('%Y-%m-%d'), 'id': 'id_return_date'
    }))
    pickup_location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Pickup Address or City'
    }))
    return_location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Drop Address or City'
    }))

    class Meta:
        model = Booking
        fields = ['pickup_date', 'return_date', 'pickup_location', 'return_location']

    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        return_date = cleaned_data.get('return_date')

        if pickup_date and pickup_date < date.today():
            self.add_error('pickup_date', "Pickup date cannot be in the past.")

        if pickup_date and return_date and pickup_date >= return_date:
            self.add_error('return_date', "Return date must be after the pickup date.")

        return cleaned_data

class PaymentMockForm(forms.Form):
    payment_method = forms.ChoiceField(choices=Payment.METHOD_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'form-check-input'
    }))
    card_number = forms.CharField(required=False, max_length=19, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '0000 0000 0000 0000', 'id': 'card_number_input'
    }))
    card_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Cardholder Name', 'id': 'card_name_input'
    }))
    card_expiry = forms.CharField(required=False, max_length=5, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'MM/YY', 'id': 'card_expiry_input'
    }))
    card_cvv = forms.CharField(required=False, max_length=4, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'CVV', 'id': 'card_cvv_input'
    }))
    paypal_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'PayPal Email Address', 'id': 'paypal_email_input'
    }))

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')

        if method == 'Card':
            if not cleaned_data.get('card_number') or not cleaned_data.get('card_expiry') or not cleaned_data.get('card_cvv'):
                raise forms.ValidationError("Please fill out all credit/debit card fields.")
        elif method == 'PayPal':
            if not cleaned_data.get('paypal_email'):
                raise forms.ValidationError("Please provide your PayPal email address.")
        
        return cleaned_data
