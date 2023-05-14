# Menubar

Initializing a `<button>` menubar with `<ul hidden role='menu'>`

## Required Blueprint

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

## Sample :material-language-javascript: + :simple-django: Implementation

```jinja title="doSelect(id-of-container-node)" linenums="1" hl_lines="5"
<script src="{% static 'doDropCommon.js' %}"></script> {# (1) #}
<script src="{% static 'doDropMenu.js' %}"></script> {# (2) #}
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

1. Common script to both menubar and listbox
2. Specific script enabling `doMenu()`

## Selector Styling

When an `<li>` on the menubar receives `:focus`:

1. `data-ok='true'` appears on `<li>`.
2. `data-ok='false'` is set on the other `<li>`
3. `aria-activedescendant` appears on `<ul>` pointing to the auto-generated id of `<li>`.

These can then be used as a selector to style the focused element.
