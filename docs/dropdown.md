# chooseDown.js

`chooseDown(domNodeID)` function is a naive, beta implementation of a dropdown element:

```jinja title="{{idx}} needs button, ul, child li options"
{% load static %}
<script src="{% static 'chooseDown.js' %}"></script> {# (1) #}
<script>chooseDown("{{idx}}")</script>
```

The list is shown via dropdown whenever the button is clicked / tapped (and hidden the same way). Based on the events on the opened list, it'll issue a custom event `userHasChosen` to the focused choice from either a "menu" or a "listbox". The choice results in the hiding of the list and the updating of the real select field.

!!! note "Reusable menu/list toggle that results in a toggle with aria-*"

    A logged-in user will have a dropdown showcasing a sub-navigation menu of: (1) Private Settings, (2) Public Profile, and (3) Logout. This is as a [menu bar](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/).

    The contact form contains a category field which, when clicked, shows a dropdown of choices: (1) Code Feedback, (2) Bug Report, and (3) Work Inquiry. This pattern, meanwhile, is a [listbox](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/).

    Since both contain similar events, _e.g. keyboard navigation, touch events, mouse clicks/hover_, I've tried my hand at some vanilla js to implement the common events without css being applied. As much as I'd like to have used a [headlessui](https://github.com/tailwindlabs/headlessui/discussions/984?sort=top) library, there doesn't seem to be one for non-js-frameworks so ended up creating a makeshift solution.

## Logic

_Before_ the `userHasChosen` event is emitted, all nodes in the list are marked:

1. `aria-selected=false` (listbox); or
2. `data-ok=false` (menu)

_After_ the `userHasChosen` event is emitted, _at least one of the nodes in the list_ will be marked:

1. `aria-selected=true` (listbox); or
2. `data-ok=true` (menu)

This indicates that the element has received the user's selection and thus can be styled accordingly and handle other events, if desired. In a "menu", the target may have a child `<a>` that needs to be clicked. In a "listbox", the target may be used as part of a form select input.

So instead of handling everything in the function, `userHasChosen` is a signal to the DOM that the user has indicated a choice from either "menu" or the "listbox".
