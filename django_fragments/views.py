from django.contrib import messages
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.views.generic import FormView, TemplateView

from .forms import ContactForm, HTMXMessageForm
from .utils import is_htmx


@require_POST
def send_msg(request: HttpRequest):
    ctx = {"htmx_msg_form": HTMXMessageForm()}
    if is_htmx(request):
        if msg := request.POST.get("message"):
            level = int(request.POST.get("tag", 10))
            messages.add_message(request, level, msg)
    return TemplateResponse(request, "msg_form.html", ctx)


class HomePage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["htmx_msg_form"] = HTMXMessageForm()
        return context


class AboutPage(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # uses missing.css extra tags, see https://missing.style/docs/colorways/
        messages.add_message(
            self.request, messages.DEBUG, "Test", extra_tags="color plain"
        )  # won't be displayed since DEBUG is not record as default, can change via
        # https://docs.djangoproject.com/en/dev/ref/contrib/messages/#changing-the-minimum-recorded-level-per-request
        messages.add_message(
            self.request, messages.INFO, "You are now informed", extra_tags="color info"
        )
        messages.add_message(
            self.request, messages.WARNING, "You warned", extra_tags="color warn"
        )
        messages.add_message(
            self.request, messages.ERROR, "I'm an error!", extra_tags="color bad"
        )
        messages.add_message(
            self.request, messages.SUCCESS, "I worked.", extra_tags="color ok"
        )
        return context


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
