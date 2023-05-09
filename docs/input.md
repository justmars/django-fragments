# `{% input %}`

## Concept

`input` customizes a [BoundField](https://docs.djangoproject.com/en/dev/ref/forms/api/#bound-and-unbound-forms) for rendering.

Any applicable tweaks done by [django_widget_tweaks](https://github.com/jazzband/django-widget-tweaks) in the invocation of `{% input ... %}` are respected prior to template expansion.

=== "_before_: :simple-django: fragment"

    ```jinja title="Invocation via Django Template Language" linenums="1" hl_lines="3"
    <form method="post" action="{% url 'account_signup' %}">
      {% csrf_token %}
      {# (1) #}
      {% input field=form.email|attr:"required"|attr:"placeholder" wrapper_kls="fld" %}
      {# single input = multiple html tags #}
      ...
    </form>
    ```

    1. Note `fld`. This enables future styling to related css targets:
        1. `.fld > ul.errorlist`
        2. `.fld span.help_css`
        3. `.fld span.help_css`

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context." linenums="1" hl_lines="3 4 5 6 7"
    <form method="post" action="/accounts/signup/">
      <input type="hidden" name="csrfmiddlewaretoken" value="xxx">
      <div> {# how the input field is rendered #}
        <label for="id_email">E-mail</label>
        <input type="email" name="email" placeholder="" autocomplete="email" required="" id="id_email">
        <span class="flex items-center font-small tracking-wide text-pink-500 text-xs mt-1 ml-1"></span>
      </div>
      ...
    </form>
    ```

::: django_fragments.templatetags.fragments.input
