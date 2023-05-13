/** Refers to `<html class="">` */
const baseKlass = document.documentElement.classList;

function setTheme(val) {
  baseKlass.add(val);
  localStorage.setItem("theme", val);
}

/** Check if localStorage populated then adjust <html> accordingly; if not available,
 *  determine user preference, finally default to light mode.
 */
function themeHTML() {
  if (localStorage.getItem("theme") === "dark") {
    baseKlass.add("dark");
  } else if (localStorage.getItem("theme") === "light") {
    baseKlass.add("light");
  } else if (window.matchMedia("(prefers-color-scheme: dark)")) {
    setTheme("dark");
  } else {
    setTheme("light");
  }
}

/** Based on `baseKlass`, toggle its opposite, e.g. if 'light', make 'dark' then
 * storage the result in LocalStorage under `theme` variable.
 */
function toggleTheme() {
  if (baseKlass.contains("dark")) {
    baseKlass.remove("dark");
    setTheme("light");
  } else if (baseKlass.contains("light")) {
    baseKlass.remove("light");
    setTheme("dark");
  }
}
