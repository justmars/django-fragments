from django.urls import path
from django.urls.resolvers import URLPattern

from .views import ContactFormView, HomePage

app_name = "test_fragments"
urlpatterns: list[URLPattern] = [
    path(route="contact/", view=ContactFormView.as_view(), name="contact"),
    path(route="", view=HomePage.as_view(), name="test_page"),
]
