# Alert

## Inclusion

:simple-django: `messages` framework can be included in a base template:

```jinja title="hq = DOM element id in base.html" linenums="1" hl_lines="4"
...
{% load fragments %}{# for the icon #}
<div id="hq" {% if messages %}hx-swap-oob="true"{% endif %} role="alert">
  {% for message in messages %}
    <div id="msg-{{forloop.counter}}" class="{{message.tags}}" data-level="{{message.level_tag|lower}}"
        _="on load show me then wait 3s then hide me then remove me">
      {{message}}
      <button id="msg-close-{{forloop.counter}}" type="button" _="on click remove #msg-{{forloop.counter}} end">
        {% icon name='x_mark_mini' css="h-5 w-5 " pre_text="Close" pre_class="sr-only" aria_hidden="true" %}
      </button>
    </div>
  {% endfor %}
</div>
{% endspaceless %}
```

## Implementation

### Generic Base Template

Because of a global alerts center in base template described above, a message can alert the user whenever `messages` are included in the context of a _traditional_ request-response cycle, e.g. `messages.add(request, messages.INFO, 'This is important!')`

### Partial Swapping Template

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

## Selector Styling

```py title="Typical Django view to add messages uses missing.style's color tags"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.add_message(
            self.request, messages.DEBUG, "Test", extra_tags="color plain"
        )  # (1)
        messages.add_message(
            self.request, messages.INFO, "You are now informed", extra_tags="color info"
        )
        messages.add_message(
            self.request, messages.WARNING, "You warned", extra_tags="color warn"
        )
        ...
        return context
```

1. won't be displayed since DEBUG is not record as default, can change though [per request](https://docs.djangoproject.com/en/dev/ref/contrib/messages/#changing-the-minimum-recorded-level-per-request)

```html title="Resulting html fragments"
<section id="hq" hx-swap-oob="true" aria-live="assertive">
  <div id="msg-1" class="color info info" data-level="info" _="on load show me ">
      You are now informed
      <button id="msg-close-1" type="button" _="on click remove #msg-1 end"><span class="sr-only">Close</span><svg aria-hidden="true">...</svg>
      </button>
    </div>
    <div id="msg-2" class="color warn warning" data-level="warning" _="on load show me ">
      You warned
      <button id="msg-close-2" type="button" _="on click remove #msg-2 end"><<span class="sr-only">Close</span><svg aria-hidden="true">...</svg>
      </button>
    </div>
  </div>
</section>
```

This is based on the blueprint found in the simple `msg.html`. If modified, just ensure the inclusion of relevant tags:

```jinja title="Selectors to use" linenums="1" hl_lines="3 4"
{% for message in messages %}
  <div id="msg-{{forloop.counter}}" {# (1) #}
    class="{{message.tags}}" {# (2) #}
    data-level="{{message.level_tag|lower}}" {# (3) #}
  >{{message}}
  </div>
  ...
{% endfor }
```

1. The `id` the close button to refer to the message
2. Extra tags and the traditional message class names ('error', 'success', etc.) are included here
3. Instead of lumping it in a class, can be more deliberate and add a dedicated data-* attribute
