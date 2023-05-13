# `msg.html`

:simple-django: `messages` framework can be included in a base template:

```jinja title="hq = DOM element id in base.html" linenums="1" hl_lines="4"
...
{% load fragments %}{# for the icon #}
<section id="hq" {% if messages %}hx-swap-oob="true"{% endif %} aria-live="assertive">
  {% for message in messages %}
    <div id="msg-{{forloop.counter}}" data-level="{{message.level_tag|lower}}"
          _="on load show me then wait 3s then hide me then remove me">
      {{message}}
      <button id="msg-close-{{forloop.counter}}" type="button" _="on click remove #msg-{{forloop.counter}} end">
        {% icon name='x_mark_mini' css="h-5 w-5 " pre_text="Close" pre_class="sr-only" aria_hidden="true" %}
      </button>
    </div>
  {% endfor %}
</section>
```

## Generic Usage

Because of a global alerts center in base template described above, a message can alert the user whenever `messages` are included in the context of a _traditional_ request-response cycle, e.g. `messages.add(request, messages.INFO, 'This is important!')`

## Partial Template Usage

Outside the _traditional_ request-response cyclee, the template will likely not include the alerts center considering that only parts of the DOM are modified via an htmx swapping event.

In such cases, one can employ [`hx-swap-oob`](https://htmx.org/attributes/hx-swap-oob/). Here, a swap of the targeted area (as its usual behavior) occurs but the `out-of-band` (oob) command will enable the reuse of the identified `hq` DOM elemen... as if to tell it:

> _"new messages have arrived, show them"._

This is the import of:

```jinja title="Add this to the swapping template" linenums="1" hl_lines="2"
...
<section id="hq" {% if messages %}hx-swap-oob="true"{% endif %} aria-live="assertive">
  ...
</section>
```

In order to employ this strategy, this partial fragment needs to be included in the swap fragment.
