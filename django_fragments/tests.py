import pytest
from django.template import Context, Template

from .forms import ContactForm

icon_test = (
    '<svg class="test" fill="currentColor" viewbox="0 0 20 20"'
    ' xmlns="http://www.w3.org/2000/svg">\n<path d="M6.28 5.22a.75.75 0'
    " 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72"
    " 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10"
    ' 8.94 6.28 5.22z"></path>\n</svg>'
)
icon_aria = (
    '<svg aria-hidden="true" class="test" fill="currentColor" viewbox="0 0 20'
    ' 20" xmlns="http://www.w3.org/2000/svg">\n<path d="M6.28 5.22a.75.75 0'
    " 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72"
    " 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10"
    ' 8.94 6.28 5.22z"></path>\n</svg>'
)


@pytest.mark.parametrize(
    "template, html",
    [
        (
            (
                '{% load fragments %}{% icon name="x_mark_mini" css="test" pre_text="on'
                ' the left" %}'
            ),
            f"<span>on the left</span>{icon_test}",
        ),
        (
            (
                '{% load fragments %}{% icon name="x_mark_mini" css="test"'
                ' post_text="on the right" %}'
            ),
            f"{icon_test}<span>on the right</span>",
        ),
        (
            (
                '{% load fragments %}{% icon name="x_mark_mini" css="test"'
                ' parent_class="cover" post_text="on the right" %}'
            ),
            f'<span class="cover">{icon_test}<span>on the right</span></span>',
        ),
        (
            (
                '{% load fragments %}{% icon name="x_mark_mini" css="test"'
                ' pre_text="Close menu" pre_class="sr-only" aria_hidden="true" %}'
            ),
            f'<span class="sr-only">Close menu</span>{icon_aria}',
        ),
    ],
)
def test_icon_fragments(template, html):
    assert Template(template).render(context=Context()) == html


@pytest.mark.parametrize(
    "template, html",
    [
        (
            """{% load fragments %}{% whitespaceless %}
            <p class="  test
                        test2
                        test3  ">
                <a href="foo/">Foo</a>
            </p>{% endwhitespaceless %}""",
            '<p class="test test2 test3"><a href="foo/">Foo</a></p>',
        ),
    ],  # noqa: E501; also from [Will Gordon](https://stackoverflow.com/users/6758654/will-gordon). See [answer](https://stackoverflow.com/a/72942459)
)
def test_whitespace(template, html):
    assert Template(template).render(context=Context()) == html


@pytest.mark.parametrize(
    "data, html",
    [
        (  # unbound form, no values
            None,
            (
                '<div class="fieldWrapper data-hidden="False"'
                ' data-widget="email"><label for="id_email">Email</label><input'
                ' type="email" name="email" required id="id_email"><p'
                ' class="help">Testable form</p></div><div class="fieldWrapper'
                ' data-hidden="False" data-widget="textarea"><label'
                ' for="id_message">Message</label><textarea name="message" cols="40"'
                ' rows="3" required id="id_message"></textarea><p'
                ' class="help"></p></div>'
            ),
        ),
        (  # bound valid form, no error message list
            {"message": "Hi there", "email": "foo@example.com"},
            (
                '<div class="fieldWrapper data-hidden="False"'
                ' data-widget="email"><label for="id_email">Email</label><input'
                ' type="email" name="email" value="foo@example.com" required'
                ' id="id_email"><p class="help">Testable form</p></div><div'
                ' class="fieldWrapper data-hidden="False" data-widget="textarea"><label'
                ' for="id_message">Message</label><textarea name="message" cols="40"'
                ' rows="3" required id="id_message">Hi there</textarea><p'
                ' class="help"></p></div>'
            ),
        ),
        (  # bound invalid form, with error message list
            {"message": "Hi there", "email": "foo"},
            (
                '<div class="fieldWrapper data-hidden="False"'
                ' data-widget="email"><label for="id_email">Email</label><input'
                ' type="email" name="email" value="foo" required id="id_email"><p'
                ' class="help">Testable form</p><ul class="errorlist"><li>Enter a valid'
                ' email address.</li></ul></div><div class="fieldWrapper'
                ' data-hidden="False" data-widget="textarea"><label'
                ' for="id_message">Message</label><textarea name="message" cols="40"'
                ' rows="3" required id="id_message">Hi there</textarea><p'
                ' class="help"></p></div>'
            ),
        ),
    ],
)
def test_contact_form(data, html):
    assert ContactForm(data).render() == html  # type: ignore
