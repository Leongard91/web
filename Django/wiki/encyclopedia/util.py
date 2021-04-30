import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def turn_to_HTML(content):
    """
    Render content from readed file for inserting into HTML
    """
    # render headigs
    hashes = 6
    while hashes != 0:
        h = re.findall(r'{} (\S.*?)?\s'.format('#'* hashes), content)
        if len(h)>0:
            for n in h:
                content = re.sub(r'{}'.format('#'* hashes+' '+n), f'<h{hashes}>'+ n + f'</h{hashes}>', content)
        hashes -= 1

    # render boldface text
    b = re.findall(r'\*\*(.*?)?\*\*', content)
    if len(b)>0:
        for i in b:
            content = re.sub(r'\*\*{}\*\*'.format(i), '<b>'+ i + '</b>', content)

    # render unordered lists,
    ul = re.findall(r'\* (.*?)?\n', content)
    if len(ul)>0:
        for i in ul:
            content = re.sub(r'\* {}\n'.format(i), '<li>'+ i + '</li>', content)
        l_items_group= re.findall(r'<li>.*</li>', content)
        for n in l_items_group:
            content = re.sub(r'{}'.format(n), '<ul>'+ n + '</ul>', content)

    # render paragraphs
    if '\r\n' in content:
        p = re.findall(r'.+\r\n', content) # \n\n or \r\n dedends on typed in .md
        for i in p:
            content = re.sub(r'{}'.format(i), '<p>' + i + '</p>', content)
    p = re.findall(r'.+\n\n', content) # \n\n or \r\n dedends on typed in .md
    for i in p:
        content = re.sub(r'{}'.format(i), '<p>' + i + '</p>', content)

    # render links
    links = re.findall(r'\[.+?\)', content)
    for i in links:
        html_link = "<a href='{}'>{}</a>".format(re.findall(r'\((.+)?\)', i)[0], re.findall(r'\[(.+)?\]', i)[0])
        content = re.sub(r'\[.+?{}\)'.format(re.findall(r'\((.+?)?\)', i)[0]), html_link, content)
        
    return content

