import re

with open("app.py", encoding="utf-8") as f:
    content = f.read()

content = content.replace('use_container_width=True', 'width="stretch"')
content = content.replace('use_container_width=False', 'width="content"')

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. Occurrences fixed.")
