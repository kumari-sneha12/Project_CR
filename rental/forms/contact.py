from django import forms
from rental.models.interactions import ContactMessage, Testimonial, Review

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Full Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email Address'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Your Message...', 'rows': 5
    }))

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class TestimonialForm(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Your Name'
    }))
    designation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Designation, e.g. Freelance Developer'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Share your experience...', 'rows': 4
    }))
    rating = forms.ChoiceField(choices=[(i, f"{i} Stars") for i in range(1, 6)], widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Testimonial
        fields = ['name', 'designation', 'message', 'rating', 'avatar']

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, f"{i} Stars") for i in range(1, 6)], widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Write your review here...', 'rows': 4
    }))

    class Meta:
        model = Review
        fields = ['rating', 'comment']
