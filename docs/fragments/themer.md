# `{% themer %}`

## Concept

`{% themer %}` is an _overrideable_ theme switcher, i.e. a `<button>` surrounding two [icons](./icon.md).

- Requires [file-based requirements](./icon.md#svg-placement) of two icons to be present.
- Thin wrapper over [`{% toggle_icons %}`](../utils.md#toggle_icons) but one containing the generic defaults.
- The `<button>` implements [`toggleTheme()`](../utils.md#toggletheme).
- When set in the template without arguments, it will use defaults.

=== "_before_: :simple-django: fragment"

    ```jinja title="Usually placed in body" linenums="1" hl_lines="3"
    <script src="{% static 'doTheme.js' %}"></script>
    <html>
      {% togl icon1_css='override1' icon2_css='override2' btn_kls='override3' %}
      ...
    </html>
    ```

=== "_after_: html :simple-html5:"

    ```jinja title="Highlighted overrides" linenums="1" hl_lines="3 6 11"
    <script src="{% static 'doTheme.js' %}"></script>
    <html>
      <button onclick="toggleTheme()" type="button" class="override3" aria-label="Toggle dark mode">
        <span class="icon1_svg">
          <span class="sr-only">Light mode</span>
          <svg class="override1" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </span>
        <span class="icon2_svg">
          <span class="sr-only">Dark mode</span>
          <svg class="override2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </span>
      </button>
    </html>
    ```

## Execution

::: django_fragments.templatetags.fragments.themer
