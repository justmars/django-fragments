function doMenu(id) {
  const [container, button, nodeList, nodeItems] = isDownable([
    document.getElementById(id),
    setIndex(document.querySelector(`#${id} button`), id, "btn"),
    setIndex(document.querySelector(`#${id} ul[role=menu]`), id, "listbox"),
    setManyIds(
      document.querySelectorAll(`#${id} ul[role=menu] > li`),
      id,
      "option"
    ),
    document.querySelectorAll(`#${id} ul[role=menu] > li a`),
  ]);
  let menu = new Downable(
    button,
    nodeList,
    nodeItems,
    focusMenuNode,
    chooseMenuNode
  );
  menu.nodeList.setAttribute("aria-labelledby", button.id);
  function focusMenuNode(node) {
    menu.nodeList.removeAttribute("aria-activedescendant");
    menu.nodeOptions.forEach((el) => delete el.dataset.ok);
    node.dataset.ok = "true";
    menu.nodeList.setAttribute("aria-activedescendant", node.id);
  }
  function chooseMenuNode() {
    let node = menu.getNode();
    if (node) {
      node.querySelector("a").click();
    }
  }
}
