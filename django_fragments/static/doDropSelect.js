function doSelect(id) {
  const [
    container,
    hiddenSelect,
    label,
    button,
    buttonSpan,
    nodeList,
    nodeItems,
  ] = isDownable([
    document.getElementById(id),
    document.querySelector(`#${id} > select[hidden]`),
    setIndex(document.querySelector(`#${id} label`), id, "label"),
    setIndex(document.querySelector(`#${id} button`), id, "btn"),
    setIndex(document.querySelector(`#${id} button > span`), id, "txt"),
    setIndex(document.querySelector(`#${id} ul[role=listbox]`), id, "listbox"),
    setManyIds(
      document.querySelectorAll(`#${id} ul[role=listbox] > li`),
      id,
      "option"
    ),
  ]);
  let sel = new Downable(
    button,
    nodeList,
    nodeItems,
    focusSelectNode,
    chooseSelectNode
  );
  sel.nodeList.setAttribute("aria-labelledby", label.id);
  function focusSelectNode(node) {
    sel.nodeList.removeAttribute("aria-activedescendant");
    sel.nodeOptions.forEach((el) => el.setAttribute("aria-selected", "false"));
    node.setAttribute("aria-selected", "true");
    sel.nodeList.setAttribute("aria-activedescendant", node.id);
  }
  function chooseSelectNode() {
    let node = sel.getNode();
    if (node) {
      hiddenSelect.querySelectorAll("option").forEach((option) => {
        option.removeAttribute("selected");
        if (option.value === node.dataset.key.toString()) {
          option.setAttribute("selected", "");
          buttonSpan.innerText = node.dataset.value.toString();
        }
      });
    }
  }
}
