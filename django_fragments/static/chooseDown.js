function verifySelectable(id) {
  function setId(el, id, suffix) {
    if (!el) {
      return false;
    }
    el.setAttribute("id", `${id}-${suffix}`);
    return el;
  }
  function setManyIds(els, id, prefix) {
    if (!els) {
      return false;
    }
    for (let i = 0; i < els.length; i++) {
      setId(els[i], id, `${prefix}-${i + 1}`);
    }
    return els;
  }

  let container = document.getElementById(id) || false;
  if (!container) {
    throw "Missing container.";
  }
  let items = [
    setId(document.querySelector(`#${id} > button`), id, "btn"),
    setId(document.querySelector(`#${id} > ul`), id, "listbox"),
    setManyIds(document.querySelectorAll(`#${id} > ul > li`), id, "option"),
  ];
  for (let item of items) {
    if (!item) {
      throw "Missing element.";
    }
  }
  return items;
}

/**
 *
 * Show/hide list of nodes, issue event `userHasChosen` to focused node, this is event target.
 *
 * The list can either be a "menu" or a "listbox" so the way the target behaves will be different.
 * In a "menu", the target may have a child <a> that needs to be clicked.
 * In a "listbox", the target may be used as part of a form select input.
 *
 * The nodes are marked "aria-selected" / "data-ok" for "focus". Either of these nodes can be used as selectors
 * for any css styling to be done via inline HTML. Focus does not mean choice. Instead it implies a candidate choice
 * has been made due to browser events: a hovering effect or a up, down key press, a touch event on a mobile device, etc.
 *
 * When a valid event occurs that converts this candidate choice to the actual selected choice,
 * the node is dispatched with the a `userHasChosen` event, and nodes are re-hidden.
 *
 * @param {*} selectable_group_id
 */
function chooseDown(selectable_group_id) {
  const [button, nodeList, nodeItems] = verifySelectable(selectable_group_id);
  const arrowKeys = ["ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft"];
  const eventToEmit = new Event("userHasChosen", {
    bubbles: false,
    cancelable: false,
  });

  // add event listener to each focusable item
  const nodeOptions = Array.prototype.slice.call(nodeItems); // to use forEach
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

    console.log(`focused ${node.id}`);
  }

  // Ready button events which shows / hides / focuses nodes
  button.addEventListener(
    "blur",
    (evt) => {
      if (evt.relatedTarget) {
        console.log(`blurred: ${evt.relatedTarget.id}`);
        if (evt.relatedTarget === nodeList) {
          let node = nodeItems[parseInt(button.dataset.index) - 1];
          console.log(`matched ${node.id}`);
          node.dispatchEvent(eventToEmit);
        } else {
          nodeOptions.forEach((node) => {
            if (evt.relatedTarget.id === node.id) {
              console.log(`matched ${node.id}`);
              node.dispatchEvent(eventToEmit);
            }
          });
        }
      }
      console.log(`targeted: ${evt.target.id}`);
      if (evt.target.id === button.id) {
        /// debugger;
        let node = nodeItems[parseInt(button.dataset.index) - 1];
        console.log(`matched ${node.id}`);
        node.dispatchEvent(eventToEmit);
      }
      hideBox(evt);
    },
    false
  );
  button.addEventListener(
    "click",
    (evt) => {
      console.log(`click on: ${evt} ${evt.relatedTarget}`);
      toggleBox(evt);
    },
    false
  );
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
          let currDownIndex = parseInt(button.dataset.index);
          currDownIndex === nodeItems.length
            ? (button.dataset.index = 1)
            : (button.dataset.index = currDownIndex + 1);
          markFocus(nodeItems[parseInt(button.dataset.index) - 1], evt);
          break;

        case "ArrowUp":
        case "ArrowLeft":
          let currUpIndex = parseInt(button.dataset.index);
          currUpIndex === 1
            ? (button.dataset.index = nodeItems.length)
            : (button.dataset.index = currUpIndex - 1);
          markFocus(nodeItems[parseInt(button.dataset.index) - 1], evt);
          break;

        case "Enter":
          const currNode = nodeItems[parseInt(button.dataset.index) - 1];
          currNode.dispatchEvent(eventToEmit);
          break;
      }
    }
  });

  function toggleBox(evt) {
    evt.preventDefault();
    button.getAttribute("aria-expanded") !== "true"
      ? showBox(evt)
      : hideBox(evt);
  }

  function showBox(evt) {
    nodeList.removeAttribute("hidden");
    button.setAttribute("aria-expanded", "true");
    button.setAttribute("aria-hidden", "false");
    console.log(`show ${nodeList.id} ${evt.type}`);
    if (!button.dataset.index) button.dataset.index = 1; // if index not set
    const focusable = nodeItems[parseInt(button.dataset.index) - 1];
    if (focusable && focusable.contains(evt.target)) markFocus(focusable);
  }

  function hideBox(evt) {
    if (button.getAttribute("aria-expanded") === "true") {
      nodeList.setAttribute("hidden", "true");
      button.setAttribute("aria-expanded", "false");
      button.setAttribute("aria-hidden", "true");
    }
    console.log(`hide ${nodeList.id} ${evt.target} ${evt.type}`);
  }
}
