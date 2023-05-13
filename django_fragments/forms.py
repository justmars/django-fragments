from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _


class HTMXMessageForm(forms.Form):
    template_name = "test_snippet.html"

    class MessageTag(models.IntegerChoices):
        DEBUG = 10
        INFO = 20
        SUCCESS = 25
        WARNING = 30
        ERROR = 40

    class OtherCategory(models.IntegerChoices):
        IMPORTANT = 10
        MEH = 20
        INUTILE = 25

    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 3}))
    tag = forms.TypedChoiceField(
        label="Tag",
        choices=MessageTag.choices,
        initial=MessageTag.DEBUG,
        help_text="This is a message tag",
        widget=forms.Select(attrs={"hidden": True}),
    )
    cat = forms.TypedChoiceField(
        label="Relevance",
        choices=OtherCategory.choices,
        initial=OtherCategory.MEH,
        help_text="This is a category",
        widget=forms.Select(attrs={"hidden": True}),
    )


class ContactForm(forms.Form):
    class Category(models.TextChoices):
        YES = "yes", _("Yes, I approve")
        NO = "no", _("No, I do not")
        MAYBE = "maybe", _("I'll think about it")
        MEH = "meh", _("Won't even think")
        IGNORE = "ignore", _("No reply")

    template_name = "test_snippet.html"
    category = forms.TypedChoiceField(
        label="Thoughts",
        choices=Category.choices,
        initial=Category.NO,
        help_text="This is a category!",
        widget=forms.Select(attrs={"hidden": True}),
    )
    email = forms.EmailField(label="Email", help_text="Testable form")
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 3}))
