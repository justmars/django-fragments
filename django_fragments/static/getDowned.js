/**
 * Show/hide list of nodes, issue event `prepSelection` to focused node, this is event target.
 *
 * The list can either be a "menu" or a "listbox" so the way the target behaves will be different.
 * In a "menu", the target may have a child <a> that needs to be clicked.
 * In a "listbox", the target may be used as part of a form select input.
 *
 * The nodes are marked "aria-selected" / "data-ok" for "focus", can be used as selectors for any
 * css styling to be done via inline HTML. Focus does not mean choice. When a valid event occurs that
 * connotes choice, the node is dispatched with the custom `prepSelection` event, and nodes are re-hidden.
 *
 * @param {*} btn_id A button element represnted by its `btn_id` which contains an aria-expanded attribute which determines whether the menu should be shown or hidden
 * @param {*} overlay_id When dropdown is shown, an overlay `overlay_id` makes clicking on the same close the menu
 * @param {*} list_id The <ul> dropdown proper's `list_id` to display items that are clickable
 * @param {*} component_id Encapsulating container of button, list and overlay.
 */
function prepSelectionFromDropdown(btn_id, overlay_id, list_id, component_id) {
  const arrowKeys = ["ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft"];

  const eventToEmit = new Event("prepSelection", {
    bubbles: false,
    cancelable: false,
  });

  const component = document.getElementById(component_id) || false;
  if (!component) throw "Missing component_id";
  component.addEventListener("blur", (evt) => hideBox(evt));

  const overlay = document.getElementById(overlay_id) || false;
  if (!overlay) throw "Missing overlay_id";
  overlay.addEventListener("click", (evt) => hideBox(evt));

  const button = document.getElementById(btn_id) || false;
  if (!button) throw "Missing btn_id";

  const nodeList = document.getElementById(list_id) || false;
  if (!nodeList) throw "Missing list_id";

  const nodeListItems = nodeList.getElementsByTagName("li") || false;
  if (!nodeList) throw "Missing list_id's <li> tags";
  for (let i = 0; i < nodeListItems.length; i++)
    nodeListItems[i].setAttribute("id", `${list_id}-${i + 1}`);

  // add event listener to each focusable item
  const nodeOptions = Array.prototype.slice.call(nodeListItems); // to use forEach
  nodeOptions.forEach((node) => {
    node.addEventListener("mouseover", () => {
      markFocus(node);
      button.dataset.index = node.id.match(/\d+$/); // see keydown parity
    });

    node.addEventListener("click", (evt) => {
      node.dispatchEvent(eventToEmit);
      button.dataset.index = node.id.match(/\d+$/); // see keydown parity
      hideBox(evt);
    });

    node.addEventListener("touchstart", (evt) => {
      evt.preventDefault(); // without this, will auto-mouse click
      markFocus(node, evt);
      button.dataset.index = node.id.match(/\d+$/); // see keydown parity
      node.dispatchEvent(eventToEmit);
      hideBox(evt); // unlike mouseover, proceed to select
    });
  });

  /**
   * Clears <li> attributes, marks proper focus. Ensures "aria-selected" for listbox types and "[data-ok]"
   * for menuitem types. that can be styled with css accordingly.
   * @param {*} node
   * @param {*} evt
   */
  function markFocus(node, evt) {
    if (node.parentNode !== nodeList)
      throw `${node} should be part of ${nodeList}`;
    nodeList.removeAttribute("aria-activedescendant"); // remove active
    nodeOptions.forEach((el) => {
      if (nodeList.getAttribute("role") === "listbox")
        el.setAttribute("aria-selected", "false");
      delete el.dataset.ok;
    });
    if (nodeList.getAttribute("role") === "listbox") {
      node.setAttribute("aria-selected", "true");
    }
    node.dataset.ok = "true";
    nodeList.setAttribute("aria-activedescendant", node.id); // assign active
    if (evt && evt.type === "keydown" && arrowKeys.includes(evt.key))
      node.scrollIntoView({
        block: "start",
        inline: "nearest",
      }); // keydown into middle of long item list

    // console.log(`focused ${node.id}`);
  }

  // Ready button events which shows / hides / focuses nodes
  button.addEventListener(
    "blur",
    (evt) => {
      if (evt.relatedTarget === nodeList) {
        // console.log(`clicked on list ${evt}`);
        let clicked_node = nodeListItems[parseInt(button.dataset.index) - 1];
        // console.log(`matched ${clicked_node}`);
        clicked_node.dispatchEvent(eventToEmit);
      }
      hideBox(evt);
    },
    false
  );
  button.addEventListener("click", (evt) => toggleBox(evt), false);
  button.addEventListener("touchstart", (evt) => {
    evt.preventDefault(); // without this, will auto-mouse click
    toggleBox(evt);
  });
  button.addEventListener("keydown", (evt) => {
    if (!button.dataset.index) button.dataset.index = 1; // if index not set
    if (button.getAttribute("aria-expanded") === "true") {
      switch (evt.key) {
        case "Tab":
        case "Escape":
          hideBox(evt);
          break;

        case "ArrowDown":
        case "ArrowRight":
          currIndex = parseInt(button.dataset.index);
          currIndex === nodeListItems.length
            ? (button.dataset.index = 1)
            : (button.dataset.index = currIndex + 1);
          markFocus(nodeListItems[parseInt(button.dataset.index) - 1], evt);
          break;

        case "ArrowUp":
        case "ArrowLeft":
          currIndex = parseInt(button.dataset.index);
          currIndex === 1
            ? (button.dataset.index = nodeListItems.length)
            : (button.dataset.index = currIndex - 1);
          markFocus(nodeListItems[parseInt(button.dataset.index) - 1], evt);
          break;

        case "Enter":
          const currNode = nodeListItems[parseInt(button.dataset.index) - 1];
          currNode.dispatchEvent(eventToEmit);
          break;
      }
    }
  });

  function toggleBox(evt) {
    button.getAttribute("aria-expanded") !== "true"
      ? showBox(evt)
      : hideBox(evt);
  }
  function showBox(evt) {
    overlay.removeAttribute("hidden");
    nodeList.removeAttribute("hidden");
    button.setAttribute("aria-expanded", "true");
    button.setAttribute("aria-hidden", "false");
    // console.log(`show ${list_id} ${evt.type}`);
    if (!button.dataset.index) button.dataset.index = 1; // if index not set
    const focusable = nodeListItems[parseInt(button.dataset.index) - 1];
    if (focusable && focusable.contains(evt.target)) markFocus(focusable);
  }
  function hideBox(evt) {
    if (button.getAttribute("aria-expanded") === "true") {
      overlay.setAttribute("hidden", "true");
      nodeList.setAttribute("hidden", "true");
      button.setAttribute("aria-expanded", "false");
      button.setAttribute("aria-hidden", "true");
    }
    // console.log(`hide ${list_id} ${evt.target} ${evt.type}`);
  }
}
