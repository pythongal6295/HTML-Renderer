"""
test code for html_render.py

This is just a start -- you will need more tests!
"""

import io
import pytest

# import * is often bad form, but makes it easier to test everything in a module.
from html_render import *


# utility function for testing render methods
# needs to be used in multiple tests, so we write it once here.
def render_result(element, ind=""):
    """
    calls the element's render method, and returns what got rendered as a
    string
    """
    # the StringIO object is a "file-like" object -- something that
    # provides the methods of a file, but keeps everything in memory
    # so it can be used to test code that writes to a file, without
    # having to actually write to disk.
    outfile = io.StringIO()
    # this so the tests will work before we tackle indentation
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()

def test_str_wrapper():
    '''
    tests a string can render like an element
    '''

    sw = StringWrapper('this is some text')

    result = render_result(sw)

    assert result == 'this is some text'

########
# Step 1
########

def test_init():
    """
    This only tests that it can be initialized with and without
    some content -- but it's a start
    """
    e = Element()

    e = Element("this is some text")


def test_append():
    """
    This tests that you can append text

    It doesn't test if it works --
    that will be covered by the render test later
    """
    e = Element("this is some text")
    e.append("some more text")

def test_render_element_one_content():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.

    this should create:
    <html> this is some text </html>
    """
    
    e = Html("this is some text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    print(file_contents)

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<!DOCTYPE html>")
    #assert file_contents.startswith("<html>")
    assert '<html>' in file_contents
    assert file_contents.endswith("</html>")

    # making sure the content got in there.
    assert("this is some text") in file_contents


def test_render_element():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.
    """
    e = Html("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    print(file_contents)
    # making sure the content got in there.
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<!DOCTYPE html>")
    assert file_contents.endswith("</html>")

def test_append_none():
    '''
    tests that a ValueError is raised if the program/user appends nothing to the list of contents
    '''
    e = Element()
    with pytest.raises(ValueError):
        e.append(None)

# # Uncomment this one after you get the one above to pass
# # Does it pass right away?
#same as test_render_element()
def test_render_element2():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.
    """
    e = Html()
    e.append("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<!DOCTYPE html>")
    assert '<html>' in file_contents
    assert file_contents.endswith("</html>")



# # ########
# # # Step 2
# # ########

# tests for the new tags
def test_html():
    '''
    test that the html tag renders correctly,and
    content can be appended to the html element and rendered
    '''
    e = Html("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()
    print(file_contents)
    
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert file_contents.endswith("</html>")


def test_body():
    '''
    test that the body tag renders correctly,and
    content can be appended to the html element and rendered
    '''
    e = Body("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<body>")
    assert file_contents.endswith("</body>")


def test_p():
    '''
    test that the p tag renders correctly,and
    content can be appended to the html element and rendered
    '''
    e = P("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<p>")
    assert file_contents.endswith("</p>")


def test_head():
    '''
    test that the head tag renders correctly with meta tag always first,and
    content can be appended to the html element and rendered
    '''
    e = Head("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()
    print(file_contents)

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<meta>")
    assert '<head>' in file_contents
    assert file_contents.endswith("</head>")


def test_sub_element():
    """
    tests that you can add another element and still render properly
    """
    page = Html()
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents) # so we can see it if the test fails

    # note: The previous tests should make sure that the tags are getting
    #       properly rendered, so we don't need to test that here.
    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    # but make sure the embedded element's tags get rendered!
    assert "<p>" in file_contents
    assert "</p>" in file_contents



########
# Step 3
########

# Add your tests here!
def test_title():
    '''
    this should look like:
    <title> Python Class Sample page </title>
    '''
    t = Title('Python Class Sample page')

    file_contents = render_result(t).strip()

    print(file_contents)
    assert file_contents.startswith('<title>')
    assert file_contents.endswith('</title>')
    assert not '\n' in file_contents

def test_title_extra():
    t = Title('Python Class Sample page')
    with pytest.raises(TypeError):
        t.append('more title')

    file_contents = render_result(t).strip()

    print(file_contents)
    assert file_contents.startswith('<title>')
    assert file_contents.endswith('</title>')
    assert not ('\n' in file_contents)


def test_title_add_later():
    t = Title()

    t.append('one title')

    file_contents = render_result(t).strip()

    print(file_contents)
    assert file_contents.startswith('<title>')
    assert file_contents.endswith('</title>')
    assert not '\n' in file_contents


# def test_attributes():
#     #another attribute test was added (test_attriubutes_dict)
#     #_class instead of class b/c class is a keyword in Python or put it in a dict
#     #or could use a dictionary
#     '''
#     <html id="TheList" style="Line-height:200%"> some text content </html>
#     '''
#     h = Html("some text content", id="TheList", style="line-height:200%")
#     file_contents = render_result(h).strip()
#     print(file_contents)
    
#     assert "some text content" in file_contents
#     assert 'id="TheList"' in file_contents
#     assert 'style="line-height:200%"' in file_contents
#     assert file_contents.startswith('<html ')
#     assert file_contents.endswith('</html>')


def test_attributes_dict():
    #another attribute test was added (test_attriubutes_dict)

    '''
    <html class="error" id="TheList" style="Line-height:200%"> some text content </html>
    '''
    
    attributes = {"class": "error",
                  "id": "TheList",
                  "style": "Line-height:200%"}

    h = Html("some text content", **attributes)
    file_contents = render_result(h).strip()
    print(file_contents)
    
    assert 'some text content' in file_contents
    assert "class='error'" in file_contents
    assert "id='TheList'" in file_contents
    assert "style='Line-height:200%'" in file_contents
    assert file_contents.startswith('<!DOCTYPE html>')
    assert '<html ' in file_contents
    assert file_contents[file_contents.index("<html"):file_contents.index("200%'>")].count(" ") == 3
    assert file_contents.endswith('</html>')


def test_hr():
    """a simple horizontal rule with no attributes"""
    hr = Hr()
    file_contents = render_result(hr)
    print(file_contents)
    assert file_contents == '<hr />\n'


def test_hr_attr():
    """a horizontal rule with an attribute"""
    hr = Hr(width='400')
    file_contents = render_result(hr)
    print(file_contents)
    assert file_contents == "<hr width='400' />\n"


def test_br():
    br = Br()
    file_contents = render_result(br)
    print(file_contents)
    assert file_contents == "<br />\n"


def test_content_in_br():
    with pytest.raises(TypeError):
        br = Br("some content")


def test_append_content_in_br():
    with pytest.raises(TypeError):
        br = Br()
        br.append("some content")


def test_A():
    a = A("http://google.com", "link to google")
    file_contents = render_result(a).strip()
    #assert file_contents == '<a href="http://google.com">link to google</a>'
    print(file_contents)
    
    assert "href='http://google.com'>link to google" in file_contents
    assert file_contents.startswith('<a ')
    assert file_contents[:file_contents.index(">")].count(" ") == 1
    assert file_contents.endswith('</a>')
    assert not '\n' in file_contents


def test_Ul():
    attributes = {"style":"line-height:200%", "id":"TheList"}
    
    ul = Ul('some list content', **attributes)
    
    file_contents = render_result(ul).strip()
    print(file_contents)
    
    assert "some list content" in file_contents
    assert "style='line-height:200%'" in file_contents
    assert "id='TheList'" in file_contents
    assert file_contents.startswith('<ul ')
    assert file_contents.endswith('</ul>')
    assert file_contents[:file_contents.index(">")].count(" ") == 2


def test_li():

    li = Li('This is the first item')

    file_contents = render_result(li).strip()
    print(file_contents)

    assert file_contents.startswith('<li>')
    assert 'This is the first item' in file_contents
    assert file_contents.endswith('</li>')


def test_li_attributes():
    attributes = {"style":"color: red"}
    
    li = Li('This is the second item', **attributes)
    
    file_contents = render_result(li).strip()
    print(file_contents)
    
    assert "This is the second item" in file_contents
    assert "style='color: red'" in file_contents
    assert file_contents.startswith('<li ')
    assert file_contents.endswith('</li>')
    assert file_contents[:file_contents.index(">")].count(" ") == 2


def test_li_within_ul():
    ul_attributes = {"style":"line-height:200%", "id":"TheList"}
    li_attributes = {"style":"color: red"}
    
    li_1 = Li('This is the first item')
    li_2 = Li('This is the second item', **li_attributes)
    
    ul = Ul(li_1, **ul_attributes)
    ul.append(li_2)
    
    file_contents = render_result(ul).strip()
    print(file_contents)
    
    assert file_contents.startswith('<ul ')
    assert file_contents.endswith('</ul>')
    assert "style='line-height:200%'" in file_contents
    assert "id='TheList'" in file_contents
    assert 'This is the first item' in file_contents
    assert "This is the second item" in file_contents
    assert "style='color: red'" in file_contents

def test_header():
    h = H(1, "This is a header")
    
    file_contents = render_result(h).strip()
    print(file_contents)
    
    assert file_contents.startswith('<h1>')
    assert 'This is a header' in file_contents
    assert file_contents.endswith('</h1>')
    assert not ('\n' in file_contents)


def test_meta():
    attributes = {"charset": "UTF-8"}
    m = Meta(**attributes)
    
    file_contents = render_result(m)
    print(file_contents)
    
    assert file_contents == "<meta charset='UTF-8' />\n"

####################
#indentation testing
# Uncomment for Step 9 -- adding indentation
####################


def test_indent():
    """
    Tests that the indentation gets passed through to the renderer
    """
    html = Html("some content")
    file_contents = render_result(html, ind="   ").rstrip()  #remove the end newline

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[0].startswith("   <")
    print(repr(lines[-1]))
    assert lines[-1].startswith("   <")


def test_indent_contents():
    """
    The contents in a element should be indented more than the tag
    by the amount in the indent class attribute
    """
    html = Element("some content")
    file_contents = render_result(html, ind="")

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[1].startswith(Element.indent)


def test_multiple_indent():
    """
    make sure multiple levels get indented fully
    """
    body = Body()
    body.append(P("some text"))
    html = Html(body)

    file_contents = render_result(html)

    print(file_contents)
    lines = file_contents.split("\n")
    for i in range(3):  # this needed to be adapted to the <DOCTYPE> tag
        assert lines[i + 1].startswith(i * Element.indent + "<")

    assert lines[4].startswith(3 * Element.indent + "some")


def test_element_indent1():
    """
    Tests whether the Element indents at least simple content

    we are expecting to to look like this:

    <html>
        this is some text
    <\html>

    More complex indentation should be tested later.
    """
    e = Element("this is some text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents

    # break into lines to check indentation
    lines = file_contents.split('\n')
    # making sure the opening and closing tags are right.
    assert lines[0] == "<html>"
    # this line should be indented by the amount specified
    # by the class attribute: "indent"
    assert lines[1].startswith(Element.indent + "thi")
    assert lines[2] == "</html>"
    assert file_contents.endswith("</html>")
