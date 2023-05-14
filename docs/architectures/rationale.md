# Architecture vs. Template Fragment

## Rationale

Instead of using a template fragment to build the component, this library considers an additional approach to locality.

A custom template tag, unfortunately, has limited support for nested DOM elements.

It might be better to just generate the necessary component via vanilla javascript so that `aria-*` based attributes and event listeners for `hover`, `click`, `keydown` are automatically added.

!!! warning "Not yet feature complete."

    As much as I'd like to have used a [headlessui](https://github.com/tailwindlabs/headlessui/discussions/984?sort=top) library, there doesn't seem to be one for non-js-frameworks so ended up creating a makeshift solution.

    In stark contrast with locality of behavior, this approach appears to hew more closely to "separation of concerns" but I think it's acceptable. Would have preferred hyperscript here but it became too unwieldy. This attempts to replicate the ARIA recommendations but not everything has been adopted (yet).

## Blueprints

!!! tip "`aria-*` attributes as `css` selectors."

    Ideally, :simple-django:-based template fragment conforms to accessibility specification :octicons-accessibility-inset-16:. To me this enables some DX benefits:

    1. Learning about accessibility and when its attributes [ought to be used](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/); and
    2. Using accessibility attributes as css selector for stylingm thereby complementing utility-css classes.

Pattern | Docs | Example
:--|:--:|:--
[alert](https://www.w3.org/WAI/ARIA/apg/patterns/alert/) | :simple-django: / htmx [alerts](./alert.md) | See example in `msg_form.html`
[listbox](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/) | :material-language-javascript: [fake select](./listbox.md) | A listbox dropdown typically appears in a `<form>`. See `down-list.html` - hides (but still uses) a real `<select>` field in the DOM, displaying a styleable alternative. Here the `<ul>` has a role of `listbox` and each child item the role of `option`.
[menubar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/) | :material-language-javascript: [button toggle](./menubar.md) | A menu bar typicaly appears in the `<nav>`. See sample  in `_nav.html` - `<ul>` has a role of `menu` and each child item the role of `menuitem`.

Since both _listbox_ and _menubar_ patterns contain similar events, _e.g. keyboard navigation, touch events, mouse clicks/hover_, I've tried my hand at some vanilla `.js` that can be included as static files in django-based templates.

## Usage

Copy/paste the "blueprint" based on the following requisites:

1. The javascript files are included as part of the static resources on the client, e.g `theFunction(elem_id)` becomes usable inline html.
2. It's necessary that the DOM nodes follow a specific "blueprint" for invoking javascript function.
3. An invocation is made so that the javascript function can be reused by multiple elements, e.g. via hyperscript:`<div id="xyz" _="on load js theFunction('xyz') end">`

!!! success "DX Benefit"

    Since the component functionality is addressed via scripting (well, mostly anyway), this enables the developer to focus on styling a fragment with the available selectors and other layouting techniques, e.g. adding containing `<div>`s where appropraite.
