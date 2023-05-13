# Utils

These are an assortment of tools in the same vein of [django-extensions](https://github.com/django-extensions/django-extensions):

## Theme helpers

Instead of placing the javascript file in its proper place within the base, I opt to place it at the top before the html tag even loads. This allows me to insert a `themeHTML()` command to get the user preference for theme and place it in localStorage, or use an existing theme, if localStorage is already populated.

```jinja title="doSelect(id-of-container-node)" linenums="1" hl_lines="3 5"
<!DOCTYPE html>
<script src="{% static 'doTheme.js' %}"></script>
<script>themeHTML()</script> {# before <html>: prevent flicker #}
<html lang="en"> {# class populated / changed  #}
  <button onclick=toggleTheme()>Theme</button> {# will toggle #}
  ...
</html>
```

So even before the `<html>` loads the following script gets executed:

```html title="base.html"
<script>
  // document.documentElement = <html> tag
  // if local storage set, use it; check user pref; if still unset: light mode
  if (localStorage.getItem("theme") === "dark") {
    document.documentElement.classList.add("dark");
  } else if (localStorage.getItem("theme") === "light") {
    document.documentElement.classList.add("light");
  } else if (window.matchMedia("(prefers-color-scheme: dark)")) {
    document.documentElement.classList.add("dark");
    localStorage.setItem("theme", "dark");
  } else {
    document.documentElement.classList.add("light");
    localStorage.setItem("theme", "light");
  }
</script>
```

### `themeHTML()`

Will populate `<html>` with `class=light` or `class=dark` depending on localStorage and/or media preference.

### `toggleTheme()`

Will toggle the existing `<html class=?>` with `light` or `dark`.

### `{% toggle_icons %}`

=== "_before_: :simple-django: fragment"

    ```jinja title="Usually placed in body" linenums="1" hl_lines="3"
    <script src="{% static 'doTheme.js' %}"></script>
    <html>
      {% toggle_icons icon1_css='test-light' icon2_css='test-dark hello-darkness' btn_kls='btn'  %}
      ...
    </html>
    ```

=== "_after_: html :simple-html5:"

    ```jinja title="Usually placed in body" linenums="1" hl_lines="3 4 5 6 7 8 9 10 11 12"
    <script src="{% static 'doTheme.js' %}"></script>
    <html>
      <button onclick="toggleTheme()" type="button" class="btn" aria-label="Toggle dark mode">
        <span class="icon1_svg">
          <span class="sr-only">Light mode</span>
          <svg class="test-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </span>
        <span class="icon2_svg">
          <span class="sr-only">Dark mode</span>
          <svg class="test-dark hello-darkness" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </span>
      </button>
      ...
    </html>
    ```

Implements two sibling [icon](./fragments/icon.md) fragments, surrounded by a `<button>` that, when clicked, calls `toggleTheme()`.

::: django_fragments.templatetags.fragments.toggle_icons

## htmx

These are just convenience fragments for oft-repeated idioms of :simple-django: + [htmx](https://htmx.org). For a more comprehensive library, see [django-htmx](https://github.com/adamchainz/django-htmx).

### `{% htmx_csrf %}`

=== "_before_: :simple-django: fragment"

    ```jinja title="Usually placed in body" linenums="1" hl_lines="5"
      <html>
        <head>
          ...
        </head>
        <body {% htmx_csrf %} class="container">
      </html>
    ```

=== "_after_: html :simple-html5:"

    ```jinja title="Usually placed in body" linenums="1" hl_lines="5"
      <html>
        <head>
          ...
        </head>
        <body hx-headers='{"X-CSRFToken": "the-token-itself"}' class="container">

      </html>
    ```

::: django_fragments.templatetags.helpers.htmx_csrf

### `is_htmx`

Checks if a request contains the `HTTP_HX_REQUEST` Header:

```py title="Usable in a view"
@require_POST
def send_msg(request: HttpRequest):
    if is_htmx(request):
        ...
```

::: django_fragments.utils.is_htmx

## Whitespaceless

Remove whitespace from template tag via a Stackover flow answer from one [Will Gordon](https://stackoverflow.com/users/6758654/will-gordon). See [answer](https://stackoverflow.com/a/72942459):

=== "_before_: :simple-django: fragment"

    ```jinja title="Invocation via Django Template Language"
      {% whitespaceless %}
        <p class="  test
                    test2
                    test3  ">
            <a href="foo/">Foo</a>
        </p>
      {% endwhitespaceless %}
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context."
    <p class="test test2 test3"><a href="foo/">Foo</a></p>
    ```

## Filter Attributes

::: django_fragments.templatetags.utils.filter_attrs.filter_attrs

## Wrap Icon

=== "_before_: :simple-django: fragment"

    ```html title="raw x_mark_mini from heroicons copy/pasted"
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
      <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
    </svg>
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context."
    <span class="sr-only">Close menu</span>
    <svg aria-hidden="true" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"></path>
    </svg>
    ```

::: django_fragments.templatetags.utils.wrap_svg.wrap_svg
