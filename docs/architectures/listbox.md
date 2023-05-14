# Listbox

Faking a `<select>` with `<ul hidden role='listbox'>`

## Data source

:simple-django: nuances on what appears in the template blueprint if using :material-list-box: [Enum types](https://docs.djangoproject.com/en/dev/ref/models/fields/#field-choices-enum-types) as choices in a listbox:

### `django.db.models.IntegerChoices`

1. `{{form.field.value}}` is an integer
2. `{{field.value.label}}` is the human-readable text

### `django.db.models.TextChoices`

1. `{{field.value.label}}` will result in `None`
2. `{{field.value}}` is the human-readable text

It's possible to use [`get_FOO_display()`](https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_FOO_display) but with respect to this fake `<select>` implementation, only the `BoundField` is passed to the template fragment.

## Required Blueprint

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

## Sample :material-language-javascript: + :simple-django: Implementation

```jinja title="doSelect(id-of-container-node)" linenums="1" hl_lines="5 6 7"
{# the js requirement #}
<script src="{% static 'doDropCommon.js' %}"></script> {# (1) #}
<script src="{% static 'doDropSelect.js' %}"></script> {# (2) #}

{# idx refers to required container id with components #}
{# note the invocation via hyperscript _ #}
<div id="{{idx}}" _="on load js doSelect('{{idx}}') end end">

  {# django_widget_tweaks to supply 'hidden' #}
  {# can also modify 'hidden' from Form widget attrs #}
  {{ field }}

  {# the label requirement #}
  {{ field.label_tag }}

  {# the button requirement #}
  <button>
    <span>{{field.value.label|default:'None'}}</span>
  </button>

  {# the list requirement #}
  <ul hidden role="listbox">
    {% for choice in field.field.choices %}
      <li data-key="{{choice.0|default:'None'}}" data-value="{{choice.1}}">
        <span>{{choice.1}}</span>
      </li> {# note: required data-* attributes in each option #}
    {% endfor %}
  </ul>
</div>
```

1. Common script to both menubar and listbox
2. Specific script enabling `doSelect()`

## Selector Styling

When an `<li>` on the listbox receives `:focus`:

1. `aria-selected='true'` appears on `<li>`.
2. `aria-selected='false'` is set on the other `<li>`
3. `aria-activedescendant` appears on `<ul>` pointing to the auto-generated id of `<li>`.

These can then be used as a selector to style the focused element.
