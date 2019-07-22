import jinja2
import os
import json
from time import gmtime, strftime
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                           trim_blocks=True,
                           lstrip_blocks=True)
template = jinja.get_template("subscription-template.j2")
map_template = {}
with open('template-config.json', encoding='utf-8') as f:
    list_config = json.load(f)

for item in list_config:
    map_template[item["filter_name"]] = []
    for file in item["files"]:
        with open(file, encoding='utf-8') as f:
            for value in [line[:-1] for line in f]:
                map_template[item["filter_name"]].append(value)

map_template["version"] = strftime("%Y%m%d%H%M", gmtime())
map_template["timestamp"] = strftime("%d %b %Y %H:%M UTC", gmtime())
msg = template.render(map_template)
with open('output/subscription.txt', 'w', encoding='utf-8') as file:
    file.write(msg)
