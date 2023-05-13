/**
 * Combines base `id` with a `suffix` and store it as the id attribute of the element `el`
 * @param {*} el
 * @param {*} id
 * @param {*} suffix
 * @returns a DOM node
 */
function addSuffixId(el, id, suffix) {
  if (!el) {
    return false;
  }
  el.setAttribute("id", `${id}-${suffix}`);
  return el;
}

/**
 * Combines base `id` with a `prefix` and store it as the id attribute of all elements `els`
 * @param {*} els
 * @param {*} id
 * @param {*} prefix
 * @returns
 */
function setManyIds(els, id, prefix) {
  if (!els) {
    return false;
  }
  for (let i = 0; i < els.length; i++) {
    addSuffixId(els[i], id, `${prefix}-${i}`);
  }
  return els;
}

/**
 * Return the DOM node `items` if all are present, otherwise throw an error.
 * @param {*} items
 * @returns Array of DOM nodes.
 */
function isExists(items) {
  for (let item of items) {
    if (!item) {
      throw "Missing element.";
    }
  }
  return items;
}

class Downable {
  constructor(button, nodeList, nodeItems, focusFunc, chooseFunc) {
    this.button = button;
    this.button.setAttribute("type", "button");
    this.button.setAttribute("aria-expanded", "false");
    this.button.setAttribute("aria-haspopup", "true");
    if (!this.button.dataset.index) this.button.dataset.index = -1; // prepare for keys

    this.nodeItems = nodeItems;
    this.nodeList = nodeList;
    this.nodeList.setAttribute("aria-orientation", "vertical");
    this.nodeList.setAttribute("tab-index", "-1");

    this.focusFunc = focusFunc;
    this.chooseFunc = chooseFunc;
    this.nodeOptions = this.prepItems(nodeItems);

    this.prepButtonKeydowns();
    this.prepButtonBlur();
    this.prepButtonClick();
    this.prepButtonTouch();
  }

  getButtonIndex() {
    let val = parseInt(this.button.dataset.index);
    // console.log(`Index of node: ${val}`);
    return val;
  }

  // get candidate
  getNode() {
    let node = this.nodeItems[this.getButtonIndex()];
    // console.log(`Fetching ${node}`);
    return node;
  }

  showBox(evt) {
    // console.log(`Box shown`);
    this.nodeList.removeAttribute("hidden");
    this.button.setAttribute("aria-expanded", "true");
    this.button.setAttribute("aria-hidden", "false");
    // console.log(`show ${this.nodeList.id} ${evt.type}`);
    const focusable = this.getNode();
    if (focusable && focusable.contains(evt.target)) focusNode(focusable);
  }

  hideBox(evt) {
    if (this.button.getAttribute("aria-expanded") === "true") {
      // console.log(`Box hidden`);
      this.nodeList.setAttribute("hidden", "true");
      this.button.setAttribute("aria-expanded", "false");
      this.button.setAttribute("aria-hidden", "true");
    }
    // console.log(`hide ${this.nodeList.id} ${evt.target} ${evt.type}`);
  }

  // determine whether button is expanded and then toggle
  toggleBox(evt) {
    evt.preventDefault();
    this.button.getAttribute("aria-expanded") !== "true"
      ? this.showBox(evt)
      : this.hideBox(evt);
  }

  // get integer from node id attribute
  nodeDigit(node) {
    return node.id.match(/\d+$/);
  }

  // set node id attribute
  setButtonIndex(val) {
    this.button.dataset.index = val;
  }

  // make list options focusable via events
  prepItems(nodeItems) {
    let nodes = Array.prototype.slice.call(nodeItems);
    nodes.forEach((node) => {
      node.setAttribute("role", "option");
      node.setAttribute("aria-selected", "false");
      node.setAttribute("tab-index", "-1");

      node.addEventListener("mouseover", () => {
        this.focusFunc(node);
        this.setButtonIndex(this.nodeDigit(node)); // see keydown parity
      });

      node.addEventListener("click", (evt) => {
        this.setButtonIndex(this.nodeDigit(node)); // see keydown parity
        this.chooseFunc();
        this.hideBox(evt);
      });

      node.addEventListener(
        "touchstart",
        (evt) => {
          evt.preventDefault(); // without this, will auto-mouse click
          this.focusFunc(node, evt);
          this.setButtonIndex(this.nodeDigit(node)); // see keydown parity
          this.chooseFunc();
          this.hideBox(evt); // unlike mouseover, proceed to select
        },
        { passive: false }
      );
    });
    return nodes;
  }

  //
  prepButtonKeydowns() {
    this.button.addEventListener("keydown", (evt) => {
      if (this.button.getAttribute("aria-expanded") === "true") {
        switch (evt.key) {
          case "Tab":
          case "Escape":
            this.hideBox(evt);
            break;

          case "ArrowDown":
            let currDownIndex = this.getButtonIndex();
            currDownIndex === this.nodeItems.length - 1
              ? this.setButtonIndex(0)
              : this.setButtonIndex(currDownIndex + 1);

            let downedNode = this.getNode();
            this.focusFunc(downedNode, evt);
            downedNode.scrollIntoView({
              block: "start",
              inline: "nearest",
            }); // keydown into middle of long item list
            break;

          case "ArrowUp":
            let currUpIndex = this.getButtonIndex();
            currUpIndex === -1 || currUpIndex === 0
              ? this.setButtonIndex(this.nodeItems.length - 1)
              : this.setButtonIndex(currUpIndex - 1);

            let uppedNode = this.getNode();
            this.focusFunc(uppedNode, evt);
            uppedNode.scrollIntoView({
              block: "start",
              inline: "nearest",
            }); // keydown into middle of long item list
            break;

          case "Enter":
            this.chooseFunc();
            break;
        }
      }
    });
  }

  // Ready button events which shows / hides / focuses nodes
  prepButtonBlur() {
    this.button.addEventListener(
      "blur",
      (evt) => {
        if (evt.relatedTarget) {
          // console.log(`blurred: ${evt.relatedTarget.id}`);
          if (evt.relatedTarget === this.nodeList) {
            this.chooseFunc();
            this.hideBox(evt);
          } else {
            this.nodeOptions.forEach((node) => {
              if (evt.relatedTarget.id === node.id) {
                this.chooseFunc();
                this.hideBox(evt);
              }
            });
          }
        }
      },
      false
    );
  }

  prepButtonClick() {
    this.button.addEventListener(
      "click",
      (evt) => {
        // console.log(`click on: ${evt} ${evt.relatedTarget}`);
        this.toggleBox(evt);
      },
      false
    );
  }

  prepButtonTouch() {
    this.button.addEventListener(
      "touchstart",
      (evt) => {
        evt.preventDefault(); // without this, will auto-mouse click
        this.toggleBox(evt);
      },
      { passive: false }
    );
  }
}
