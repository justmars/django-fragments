# `{% icon %}`

## Concept

`icon` combines `<svg>` (via _named_ `*.html`) with a `<span>` (before or after) it and an optional parent tag around it.

=== "_before_: :simple-django: fragment"

    ```jinja title="Invocation via Django Template Language" linenums="1" hl_lines="5"
    {% load fragments %}
    <html>
      {# assumes heroicons as default unless modified #}
      {% icon name='x_mark_mini' aria_hidden="true" pre_text="Close menu" pre_class="sr-only"  %}
      {# re: 'x_mark_mini' (1), re: attributes (2) #}
    </html>
    ```

    1. `name='x_mark_mini'` refers to a heroicon (default) svg copy/pasted into a file named 'heroicon_x.html'
    2. The `aria_hidden` attribute is converted to `aria-hidden`, `pre_text` and `pre_class` means add a `<span class='sr-only'>Close menu<span>` __before__ _(pre_)_ the svg icon.

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context."
    <html>
      <span class="sr-only">Close menu</span>
      <svg
        aria-hidden="true" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round">
        </path>
      </svg>
    </html>
    ```

## Setup

In order to work, must configure `settings.py` (or its equivalent) to define a path and then add properly named `.html` files containing copy/pasted raw `<svg>` from sources.

```py title="src/config/_settings.py"
FRAGMENTS = {
  "icons_prefix": "heroicons", # prefix
  "icons_path": BASE_DIR / "templates" / "svg" # folder must exist, must use Path
}
```

## SVG Placement

1. Copy `<svg>` markup from a _source_ such as [heroicons](https://heroicons.com/), [bootstrap](https://icons.getbootstrap.com/), etc.;

    The svg markup in the file will look like:

      ```html title="x_mark_mini"
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
        <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
      </svg>
      ```

2. The name of the file to be created is relevant. Note _source_, we'll call this the `prefix` (see `FRAGMENTS['icons_prefix']`);
3. Create `.html` file found in `FRAGMENTS['icons_path']` in the proper folder and paste the `<svg>` markup to that file. See placement:

      ```yaml title="Prefix of source, name of svg" linenums="1" hl_lines="7"
      ...
      ├── config/
      ├── static/
      ├── templates/
          ├── svg/
              ├── bootstrap_github.html # (1)
              ├── heroicons_x_mark_mini.html # insert svg markup here (2)
              ...
      ```

      1. Dissected (prefix used) `bootstrap`; (icon name) `github`. Use as: `{% icon name='github' prefix="bootstrap" %}`

      1. Dissected:

         1. prefix used: `heroicons`
         2. icon name: `x_mark_mini`

         Use as:

         1. `{% icon name='x_mark_mini' prefix="heroicons" %}`; or
         2. `{% icon name='x_mark_mini' %}` (since heroicons is the default).

      ```html title="/src/templates/svg/heroicons_x_mark_mini.html"
      <!-- note the created file's name -->
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
        <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
      </svg>
      ```

4. Filename follows convention `prefix` + `_` + `name` (of the `<svg>` from the _source_)`.html`.
5. The user is responsible for renaming the file properly to match the `prefix` and `name`. Note the `name` must replace dashes `-` with underscores `_`.

## Basis

::: django_fragments.templatetags.fragments.icon
