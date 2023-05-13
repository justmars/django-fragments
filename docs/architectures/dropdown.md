# Single Dropdown

!!! note "Reusable menu/list toggle that results in a toggle with aria-*"

    A [menu bar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/) typicaly appears in the `<nav>`.

    A [listbox dropdown](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/) typically appears in a `<form>`.

    Since both contain similar events, _e.g. keyboard navigation, touch events, mouse clicks/hover_, I've tried my hand at some vanilla js to implement the common events without css being applied.

### listbox

Faking a `<select>` with `<ul hidden role='listbox'>`

#### listbox components

```js title="Javascript checks"
document.querySelector(id) // (1)

// Hidden field + label (2)
document.querySelector(`#${id} > select[hidden]`)
document.querySelector(`#${id} label`)

// Button with text (3)
document.querySelector(`#${id} button`)
document.querySelector(`#${id} button > span`)

// Listbox options (4)
document.querySelector(`#${id} ul[hidden][role=listbox]`)
document.querySelectorAll(`#${id} ul[hidden][role=listbox] > li`)
```

1. The container will contain component DOM nodes
2. Should contain direct child `<select hidden>` and associated `<label>` (need not be a direct child)
3. Child `<button>` with a direct child `<span>`
4. Child `<ul hidden role='listbox'>` with direct children `<li>`

#### listbox sample

```jinja title="doSelect(id-of-container-node)" linenums="1" hl_lines="4"
<script src="{% static 'doDropCommon.js' %}"></script>
<script src="{% static 'doDropSelect.js' %}"></script>
<div id="{{idx}}" _="on load js doSelect('{{idx}}') end end"> {# required container id with components #}
  {{ field }} {# can add django_widget_tweaks to supply 'hidden' or modify from Form widget attrs #}
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

#### listbox focus

When an `<li>` on the listbox receives `:focus`:

1. `aria-selected='true'` appears on `<li>`.
2. `aria-selected='false'` is set on the other `<li>`
3. `aria-activedescendant` appears on `<ul>` pointing to the auto-generated id of `<li>`.

These can then be used as a selector to style the focused element.

### menubar

Initializing a `<button>` menubar with `<ul hidden role='menu'>`

#### menubar components

```js title="Javascript checks"
document.querySelector(id) // (1)

// Button with text (2)
document.querySelector(`#${id} button`)

// Clickable menu items (3)
document.querySelector(`#${id} ul[hidden][role=menu]`)
document.querySelectorAll(`#${id} ul[hidden][role=menu] > li`)
document.querySelectorAll(`#${id} ul[hidden][role=menu] > li a`)
```

1. The container will contain component DOM nodes
2. Child `<button>`
3. Child `<ul hidden role='menu'>` with direct children `<li>` containing an `<a>` element.

#### menubar sample

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

#### menubar focus

When an `<li>` on the menubar receives `:focus`:

1. `data-ok='true'` appears on `<li>`.
2. `data-ok='false'` is set on the other `<li>`
3. `aria-activedescendant` appears on `<ul>` pointing to the auto-generated id of `<li>`.

These can then be used as a selector to style the focused element.
