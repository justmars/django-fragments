const htmlKls = document.documentElement.classList;
function themeHTML() {
  if (localStorage.getItem("theme") === "dark") {
    htmlKls.add("dark");
  } else if (localStorage.getItem("theme") === "light") {
    htmlKls.add("light");
  } else if (window.matchMedia("(prefers-color-scheme: dark)")) {
    htmlKls.add("dark");
    localStorage.setItem("theme", "dark");
  } else {
    htmlKls.add("light");
    localStorage.setItem("theme", "light");
  }
}

function toggleTheme() {
  if (htmlKls.contains("dark")) {
    htmlKls.remove("dark");
    htmlKls.add("light");
    localStorage.setItem("theme", "light");
  } else if (htmlKls.contains("light")) {
    htmlKls.remove("light");
    htmlKls.add("dark");
    localStorage.setItem("theme", "dark");
  }
}
