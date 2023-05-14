# `{% hput %}`

## Concept

`hput` customizes a [BoundField](https://docs.djangoproject.com/en/dev/ref/forms/api/#bound-and-unbound-forms) for rendering, with option to supply inline validation using the logic derived from [hernantz](#hx_enable_inline_validation).

=== "_before_: :simple-django: fragment"

    ```jinja title="Invocation via Django Template Language" linenums="1" hl_lines="3"
    <form method="post" action="{% url 'account_signup' %}">
      {% csrf_token %}
      {% hput form.email validate="/this-is-an-endpoint" %}
      ...
    </form>
    ```
=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context." linenums="1" hl_lines="3 4 5 6 7 8 9 10 11 12 13 14"
    <form method="post" action="/accounts/signup/">
      <input type="hidden" name="csrfmiddlewaretoken" value="xxx">
      <div id="hput_id_email"
        hx-select="#hput_id_email"
        hx-post="/this-is-an-endpoint"
        hx-trigger="blur from:find input"
        hx-target="#hput_id_email"
        hx-swap="outerHTML"
        class="h"
        data-widget="email">
        <label for="id_email">Email</label>
        <input type="email" name="email" required id="id_email">
        <small>Testable form</small>
      </div>
      ...
    </form>
    ```

Use of [django_widget_tweaks](https://github.com/jazzband/django-widget-tweaks) inlined with `{% hput ... %}` works:

=== "_before_: :simple-django: fragment"

    ```jinja title="Invocation via Django Template Language" linenums="1" hl_lines="1 4"
    {% load widget_tweaks %}
    <form method="post" action="{% url 'account_signup' %}">
      {% csrf_token %}
      {% hput field=form.email|attr:"placeholder=Hello World!" %}
      ...
    </form>
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context." linenums="1" hl_lines="3 4 5 6 7"
    <form method="post" action="/accounts/signup/">
      <input type="hidden" name="csrfmiddlewaretoken" value="xxx">
      <div> {# how the input field is rendered #}
        <label for="id_email">E-mail</label>
        <input type="email" name="email" placeholder="Hello World!" autocomplete="email" required id="id_email">
        <small>Testable form</small>
      </div>
      ...
    </form>
    ```

## `hx_enable_inline_validation()`

!!! warning "Requires htmx-compatible view"

    Need to handle the request, checking if it is an htmx request (see [is_htmx()](../utils.md#is_htmx)) and then render the template with the form.

::: django_fragments.templatetags.helpers.hx_enable_inline_validation
