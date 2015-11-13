# -*- coding: utf-8 -*-
import pytest

from formasaurus.html import (
    html_tostring,
    html_escape,
    remove_by_xpath,
    load_html,
    html_tostring,
    get_forms,
    get_cleaned_form_html,
    get_field_names,
    get_visible_fields,
    escaped_with_field_highlighted,
    highlight_fields,
    add_text_after,
    add_text_before,
)

FORM1 = """
<form>
    <input name='foo'/>
    <input type='text' value='hello'>
    <select name='bar'>
        <option value='hi'>hi</option>
    </select>
    <input type='radio' name='ch' value='v1'>
    <input type='radio' name='ch' value='v2'>
    <textarea name='baz'></textarea>
    <input type='submit' name='go'>
    <input type='button' name='cancel'>
    <input type='hidden' name='spam' value='123'>
    <input type='HIDDEN' name='spam2' value='123'>
</form>
"""


def test_html_tostring():
    src = "<form><input value='hello'><input type='submit'></form>"
    tree = load_html(src)
    assert html_tostring(tree) == """<form>
<input value="hello"><input type="submit">
</form>
"""


def test_get_forms():
    forms = get_forms(load_html("""
    <p>some text</p>
    <form action="/go">hi</form>
    <FORM method='post'><input name='foo'></FORM>
    """))
    assert len(forms) == 2
    assert forms[0].action == "/go"
    assert forms[1].method == "POST"


def test_get_visible_fields():
    tree = load_html(FORM1)
    form = get_forms(tree)[0]
    elems = get_visible_fields(form)
    names = get_field_names(elems)
    assert names == ['foo', 'bar', 'ch', 'baz', 'go', 'cancel']


def test_add_text_after():
    tree = load_html("<p>hello,<br/>world</p>")
    add_text_after(tree.xpath('//br')[0], "brave new ")
    add_text_after(tree.xpath('//p')[0], "!")
    assert html_tostring(tree).strip() == "<p>hello,<br>brave new world</p>!"


def test_add_text_before():
    tree = load_html("<div><p>hello<br/>world</p><i>X</i></div>")
    add_text_before(tree.xpath('//br')[0], ",")
    add_text_before(tree.xpath('//p')[0], "!")
    add_text_before(tree.xpath('//i')[0], "1")
    assert html_tostring(tree).strip() == "<div>!<p>hello,<br>world</p>1<i>X</i>\n</div>"


@pytest.mark.xfail()
def test_add_text_before_root():
    tree = load_html("<p>hello<br/>world</p>")
    add_text_before(tree.xpath('//p')[0], "!")
    assert html_tostring(tree).strip() == "!<p>hello<br>world</p>"
