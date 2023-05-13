# `{% nava %}`

## Concept

Uses [`django.utils.format_html()`](https://docs.djangoproject.com/en/dev/ref/utils/) to output an `<a>` element. When the `request` object is included in the template tag, it will call [`curr()`](#curr) to vet whether the element should include `aria-current=page`. This makes it fit for desktop/mobile navbar link.

=== "_before_: :simple-django: fragment"

    ```jinja title="Inclusion in nav via Django Template Language" linenums="1" hl_lines="3"
    <nav>
      {% nava 'home' 'Home' css="some css classes here" request=request %}
      {% nava 'about' 'About' css="some css classes here" request=request %}
    </nav>
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context." linenums="1" hl_lines="3"
    <nav><!-- Assume user is presently in the about page -->
      <a href="/home" class="some css classes here">Home</a>
      <a aria-current="page" href="/about" class="some css classes here">About</a>
    </nav>
    ```

::: django_fragments.templatetags.fragments.nava

## `curr`

::: django_fragments.templatetags.fragments.curr
