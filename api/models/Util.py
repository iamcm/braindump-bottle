import datetime 


def slugify(string):
    return string.replace(' ','-')
    
def niceDate(dt):
    return dt.strftime('%a %d %B %Y')
    
def a_wrap(content='', href='#', id=None, className=None):
    output = '<a href="%s"' % href
    if id: output += ' id="%s"' % id
    if className: output += ' className="%s"' % className
    output += '>'
    output += content
    output += '</a>'
    
    return output
