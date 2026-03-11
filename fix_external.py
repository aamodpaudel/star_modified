import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replacer(match):
        a_tag = match.group(0)
        if 'target=' in a_tag:
            return a_tag
        if 'href="http' in a_tag:
            return a_tag.replace('<a ', '<a target="_blank" ', 1)
        return a_tag
        
    new_content = re.sub(r'<a\s+[^>]*href="[^"]*"[^>]*>', replacer, content)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {file}')
print('Done.')
