# -*- coding: utf-8 -*-
import jinja2
import os
from time import gmtime, strftime
import glob

output_dir = "output/"
template_dir = "templates/"
filter_paths = [
    {
        "path": "filters/",
        "template": "template.j2",
        "output": "subscription.txt"
    },
    {
        "path": "annoyance_filters/",
        "template": "template_annoyance.j2",
        "output": "annoyance.txt"
    }
]


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader([template_dir, '.']),
    ])
    env = jinja2.Environment(
        loader=loader
    ).get_template(filename)
    env.globals['version'] = strftime('%Y%m%d%H%M', gmtime())
    env.globals['timestamp'] = strftime('%d %b %Y %H:%M UTC', gmtime())
    return env.render(context)


def write_file(rendered, path):
    with open(os.path.join(path), 'w', encoding='utf-8') as file:
        print("render:", path)
        file.write(rendered)


def main():
    os.makedirs(output_dir, exist_ok=True)
    for filter_path in filter_paths:
        filter_files = [f.replace(
            "\\", "/") for f in glob.glob(filter_path['path'] + "**/*.txt", recursive=True) if "whitelist" not in f]
        whitelist_files = [f.replace(
            "\\", "/") for f in glob.glob(filter_path['path'] + "**/*.txt", recursive=True) if "whitelist" in f]
        file_list = filter_files + whitelist_files
        rendered = render(filter_path['template'], {'file_list': file_list})
        write_file(rendered, output_dir+filter_path['output'])


if __name__ == '__main__':
    main()
