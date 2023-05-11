from django.template.response import TemplateResponse
from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    template_name = "home.html"
    form_class = ContactForm

    def form_invalid(self, form: ContactForm):
        return TemplateResponse(self.request, "home.html", {"form": form})

    def form_valid(self, form: ContactForm):
        if form.is_valid():
            print("Success!")
        return TemplateResponse(self.request, "home.html", {})


app_name = "test_fragments"
urlpatterns: list[URLPattern] = [
    path(
        route="",
        view=ContactFormView.as_view(),
        name="test_page",
    )
]
