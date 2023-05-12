# `{% og_* %}`

## og_title

=== "_before_: :simple-django: fragment"

    ```jinja title="Inclusion in nav via Django Template Language"
    {% og_title 'This is the title of my article' %}
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context."
    <title>This is the title of my article</title>
    <meta property="og:title" content="This is the title of my article"/>
    <meta name="twitter:title" content="This is the title of my article"/>
    ```

## og_desc

=== "_before_: :simple-django: fragment"

    ```jinja title="Inclusion in nav via Django Template Language"
    {% og_desc 'This is a description' %}
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context."
    <meta name="description" content="This is a description}"/>
    <meta property="og:description" content="This is a description"/>
    <meta name="twitter:description" content="This is a description"/>
    ```

## og_img

=== "_before_: :simple-django: fragment"

    ```jinja title="Inclusion in nav via Django Template Language"
    {% og_img url='http://open-graph-image-to-show' alt='Descriptive text to accompany image' %}
    ```

=== "_after_: html :simple-html5:"

    ```html title="Output HTML after the Template is populated with the Context."
    <meta property="og:image" content="http://open-graph-image-to-show"/>
    <meta property="og:image:alt" content="Descriptive text to accompany image}"/>
    <meta name="twitter:image" content="http://open-graph-image-to-show"/>
    <meta name="twitter:image:alt" content="Descriptive text to accompany image"/>
    ```
