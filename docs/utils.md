# Utils

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
