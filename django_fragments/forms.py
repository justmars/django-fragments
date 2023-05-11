from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    class Category(models.TextChoices):
        YES = "yes", _("Yes, I approve")
        NO = "no", _("No, I do not")
        MAYBE = "maybe", _("I'll think about it")
        MEH = "meh", _("Won't even think")
        IGNORE = "ignore", _("No reply")

    template_name = "test_snippet.html"
    category = forms.TypedChoiceField(
        label="Yes/No",
        choices=Category.choices,
        initial=Category.NO,
        help_text="This is a category!",
    )
    email = forms.EmailField(label="Email", help_text="Testable form")
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 3}))
