import re
content = '''# Python

Python is a programming language that can be used both for writing **command-line scripts** or building **web applications**.
'''
hashes = 6
while hashes != 0:
    h = re.findall(r'{} (\S.*?)?\s'.format('#'* hashes), content)
    if len(h)>0:
        for n in h:
            content = re.sub(r'{}'.format('#'* hashes+' '+n), f'<h{hashes}>'+ n + f'</h{hashes}>', content)
    hashes -= 1

b = re.findall(r'\*\*(.*?)?\*\*', content)
if len(b)>0:
    for i in b:
        content = re.sub(r'\*\*{}\*\*'.format(i), '<b>'+ i + '</b>', content)


ul = re.findall(r'\* (.*?)?\n', content)
if len(ul)>0:
    for i in ul:
        content = re.sub(r'\* {}\n'.format(i), '<li>' + i + '</li>', content)
    l_items_group= re.findall(r'<li>.*</li>', content)
    for n in l_items_group:
        content = re.sub(r'{}'.format(n), '<p><ul>' + n + '</ul></p>', content)

p = re.findall(r'(.+)\n\n', content) # \n\n or \r\n dedends from system
for i in p:
    content = re.sub(r'{}'.format(i), f'<p>{i}</p>', content)

links = re.findall(r'\[.+?\)', content)
for i in links:
    html_link = "<a href='{}'>{}</a>".format(re.findall(r'\((.+)?\)', i)[0], re.findall(r'\[(.+)?\]', i)[0])
    content = re.sub(r'\[.+?{}\)'.format(re.findall(r'\((.+?)?\)', i)[0]), html_link, content)
#print(links)
print(content)