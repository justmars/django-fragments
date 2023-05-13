# `msg.html`

:simple-django: `messages` framework can be included in a base template:

```jinja title="hq = DOM element id in base.html"
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

Because of a global alerts center in base template described above, a message can alert the user whenever it is included in a view in the general request-response cycle.

## Partial Template Usage

Outside the general request-response cyclee, the template will likely not include the alerts center, e.g. only parts of the DOM are modified via an htmx request.

In such cases, one can employ `hx-swap-oob` to modify the template on swap of the targeted area (as its usual behavior) but then add the `out-of-band` (oob) command ... to reuse identified `hq` DOM element as if to tell it _"new messages have arrived, show them"._
