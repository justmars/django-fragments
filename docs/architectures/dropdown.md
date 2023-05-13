# Single Dropdown

!!! note "Reusable menu/list toggle that results in a toggle with aria-*"

    A [menu bar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/) typicaly appears in the `<nav>`.

    A [listbox dropdown](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/) typically appears in a `<form>`.

    Since both contain similar events, _e.g. keyboard navigation, touch events, mouse clicks/hover_, I've tried my hand at some vanilla js to implement the common events without css being applied. As much as I'd like to have used a [headlessui](https://github.com/tailwindlabs/headlessui/discussions/984?sort=top) library, there doesn't seem to be one for non-js-frameworks so ended up creating a makeshift solution.

## Architecture-Driven

Instead of using a template fragment to compose the component, this takes another approach to locality. The `aria-*` based attributes and javascript event listeners for `hover`, `click`, `keydown` are added automatically provided:

1. The javascript files are loaded.
2. The DOM nodes follow an architecture pattern.
3. An invocation is made to consume a function within the architecture.

With component functionality separated, can focus on styling a fragment with utility classes.

### listbox

Faking a `<select>` with `<ul role='listbox'>`

```js title="Javascript checks"
document.querySelector(id) // (1)

// Hidden field + label (2)
document.querySelector(`#${id} > select[hidden]`)
document.querySelector(`#${id} label`)

// Button with text (3)
document.querySelector(`#${id} button`)
document.querySelector(`#${id} button > span`)

// Listbox options (4)
document.querySelector(`#${id} ul[role=listbox]`)
document.querySelectorAll(`#${id} ul[role=listbox] > li`)
```

1. The container will contain component DOM nodes
2. Should contain direct child `<select hidden>` and associated `<label>` (need not be a direct child)
3. Child `<button>` with a direct child `<span>`
4. Child `<ul role='listbox'>` with direct children `<li>`

```jinja title="doSelect(id-of-container-node)" linenums="1" hl_lines="4"
{% load widget_tweaks %}
<script src="{% static 'doDropCommon.js' %}"></script>
<script src="{% static 'doDropSelect.js' %}"></script>
<div id="{{idx}}" _="on load js doSelect('{{idx}}') end end"> {# required container id with components #}
  {{ field|append_attr:"hidden" }} {# select #}
  {{ field.label_tag }} {# label #}
  <button>
    <span>{{field.value.label|default:'None'}}</span>
  </button>
  <ul hidden role="listbox">
    {# required data-* attributes in each option #}
    {% for choice in field.field.choices %}
      <li data-key="{{choice.0|default:'None'}}" data-value="{{choice.1}}">
        <span>{{choice.1}}</span>
      </li>
    {% endfor %}
  </ul>
</div>
```

### menubar

Initializing a `<nav>` menubar with `<ul role='menu'>`

```js title="Javascript checks"
document.querySelector(id) // (1)

// Button with text (2)
document.querySelector(`#${id} button`)

// Clickable menu items (3)
document.querySelector(`#${id} ul[role=menu]`)
document.querySelectorAll(`#${id} ul[role=menu] > li`)
document.querySelectorAll(`#${id} ul[role=menu] > li a`)
```

1. The container will contain component DOM nodes
2. Child `<button>`
3. Child `<ul role='menu'>` with direct children `<li>` containing an `<a>` element.

```jinja title="doSelect(id-of-container-node)" linenums="1" hl_lines="5"
<script src="{% static 'doDropCommon.js' %}"></script>
<script src="{% static 'doDropMenu.js' %}"></script>
<html>
  <head>...</head>
  <nav id="nav-menu-id" _="on load js doMenu('nav-menu-id') end end"> {# required container id with components #}
    <button>Menu</button>
    <ul hidden role="menu">
      <li>
        <a href="#">Home</a> {# required a clickable #}
      </li>
      ...
    </ul>
  </nav>
  ...
</html>
```
