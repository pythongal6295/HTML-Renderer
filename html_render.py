#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:
    tag = 'html'
    indent = '    '

    def __init__(self, content=None, indent_level=0, **kwargs):
        
        #stored as a dict
        self.attributes = kwargs
        self.content = []
        self.indent_level = indent_level 
        if content is not None:
            self.append(content)
    
    
    def indent_str(self):
        #set this back to indent * indent_level
        num_indent = indent * self.indent_level
        return (num_indent * self.indent_level)


    def append(self, new_content):
        if not new_content:
            raise ValueError("cannot append nothing")
        if isinstance(new_content, str):
            new_content = StringWrapper(new_content)
        self.content.append(new_content)

    
    def _open_tag(self):
        open_tag = [f'<{self.tag}']
        open_tag.append(''.join([' {}={!r}'.format(k.replace('""', ""), v) for k,v in self.attributes.items()]))
        open_tag.append('>')
        return open_tag
    
    def _close_tag(self):
        close_tag = f'</{self.tag}>'
        return close_tag
                
    def render(self, out_file, cur_ind=0):

        out_file.write(self.indent * cur_ind)
        out_file.write(''.join(self._open_tag()))
        out_file.write('\n')
 
        for cont in self.content:
            next_ind = cur_ind + 1
            cont.render(out_file, cur_ind=next_ind)
            out_file.write('\n') 

        out_file.write(self.indent * cur_ind)
        out_file.write(self._close_tag())
        out_file.write('\n')


class StringWrapper(str):
    
    def render(self, out_file, cur_ind=0):

        out_file.write("    " * cur_ind)
        out_file.write(self)


class Html(Element):
    tag = 'html'
    doc_tag = '!DOCTYPE html'
    
    def render(self, out_file, cur_ind=0):
        out_file.write(f'<{self.doc_tag}>\n')
        super().render(out_file, cur_ind=0)


class Body(Element):
    tag = 'body'


class P(Element):
    tag = 'p'


class Head(Element):
    tag = 'head'
    
    def render(self, out_file, cur_ind=0):
        out_file.write(super().indent * cur_ind)
        out_file.write(f'<{Meta.tag}>\n')
        super().render(out_file, cur_ind=0)


class OneLineTag(Element):
    #heading, h1, h2
    def render(self, out_file, cur_ind=0):
        out_file.write(super().indent * cur_ind)
        out_file.write(''.join(self._open_tag()))
        
        self.content[0].render(out_file)
        
        out_file.write(self._close_tag())
        out_file.write('\n')

    def append(self, new_content):
        if len(self.content) > 0:
            raise TypeError('cannot append to a OneLineTag')
        super().append(new_content)
        #Element.append(self, new_content)


class Title(OneLineTag):
    tag = 'title'


class SelfClosingTag(Element):
    
    def __init__(self, content=None, **kwargs):
        if content is not None:
            raise TypeError ("SelfClosingTag can not contain any content")
        super().__init__(content=content, **kwargs)


    def render(self, out_file, cur_ind=0):
        out_file.write(super().indent * cur_ind)
        tag = "".join(self._open_tag()[:-1] + [" />\n"])
        out_file.write(tag)

    def append(self, *args):
        raise TypeError("You can not add content to a SelfClosingTag")


class Hr(SelfClosingTag):
    tag ='hr'


class Br(SelfClosingTag):
    tag = 'br'


class Meta(SelfClosingTag):
    tag = 'meta'
    
    
class A(OneLineTag):
    tag = 'a'
    
    def __init__(self, link, content=None, **kwargs):
        kwargs['href'] = link
        super().__init__(content, **kwargs)


class Ul(Element):
    tag = 'ul'

class Li(Element):
    tag = 'li'

class H(OneLineTag):
    '''class for header tag'''
    
    def __init__(self, level, content=None, **kwargs):
        self.tag = f'h{level}'
        super().__init__(content, **kwargs)
        


    
            
            