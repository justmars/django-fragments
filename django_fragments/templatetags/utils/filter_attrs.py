def filter_attrs(key: str, d: dict, unprefix: bool = False) -> dict[str, str]:
    """Filter `k`, `v` from `d` based on keys prefixed with `<key>_`. Based on this result, rename or replace the key,
    depending on the `unprefix` flag.

    This enables a shortcut for gathering all `<key>-`* attributes found in the dict `d` and parse them properly
    before inserting them into html tags.

    Examples:
        >>> res = filter_attrs(key="aria", d={"aria_hidden":"true"})
        >>> res['aria-hidden'] == "true"
        True
        >>> res_hx = filter_attrs(key="hx", d={"hx_get":"https://test.html",  "hx_target":"body"})
        >>> res_hx['hx-get'] == "https://test.html"
        True
        >>> res_hx['hx-target'] == "body"
        True
        >>> res_dt = filter_attrs(key="data", d={"data_site_good":"https://test.html"})
        >>> res_dt['data-site-good'] == "https://test.html"
        True
        >>> parent_res = filter_attrs(key="parent", d={"non-a-parent": "test", "parent_class":"flex items-center", "parent_title": "I should be centered"}, unprefix=True)
        >>> "parent_class" in parent_res
        False
        >>> "class" in parent_res
        True
        >>> "title" in parent_res
        True
        >>> "non-a-parent" in parent_res
        False
        >>> pre_res = filter_attrs(key="pre", d={"pre_class":"sr-only"}, unprefix=True)
        >>> "class" in pre_res
        True
        >>> res_btn = filter_attrs(key="btn", d={"btn_name":"i-am-button", "btn_id": "btn-1"}, unprefix=True)
        >>> res_btn["name"] == "i-am-button"
        True
        >>> res_btn["id"] == "btn-1"
        True
        >>> res_a= filter_attrs(key="a", d={"a_href":"#", "a_target": "_self"}, unprefix=True)
        >>> res_a["href"] == "#"
        True
        >>> res_a["target"] == "_self"
        True

    Args:
        d (dict): Values from a template tag.

    Returns:
        dict[str, str]: dict to be used for a html tag's aria-* attributes.
    """  # noqa: E501
    return {
        (k.removeprefix(f"{key}_") if unprefix else k.replace("_", "-")): v
        for k, v in d.items()
        if k.startswith(f"{key}_")
    }
