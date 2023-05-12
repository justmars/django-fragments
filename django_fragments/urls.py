from django.urls import path
from django.urls.resolvers import URLPattern

from .views import AboutPage, ContactFormView, HomePage, send_msg

app_name = "test_fragments"
urlpatterns: list[URLPattern] = [
    path(route="send_msg/", view=send_msg, name="send_msg"),
    path(route="contact/", view=ContactFormView.as_view(), name="contact"),
    path(route="about/", view=AboutPage.as_view(), name="about"),
    path(route="", view=HomePage.as_view(), name="test_page"),
]
