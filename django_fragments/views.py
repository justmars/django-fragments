from django.template.response import TemplateResponse
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


class HomePage(TemplateView):
    template_name = "home.html"


class AboutPage(TemplateView):
    template_name = "about.html"


class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm

    def form_invalid(self, form: ContactForm):
        return TemplateResponse(self.request, "contact.html", {"form": form})

    def form_valid(self, form: ContactForm):
        if form.is_valid():
            print("Success!")
            form = ContactForm()  # reset the form
        return TemplateResponse(self.request, "contact.html", {"form": form})
