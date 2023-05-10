from django import forms


class ContactForm(forms.Form):
    template_name = "test_snippet.html"
    email = forms.EmailField(label="Email", help_text="Testable form")
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 3}))
