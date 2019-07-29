# -*- coding: utf-8 -*-
import jinja2
import os
from time import gmtime, strftime

output_dir = "output"

@jinja2.contextfunction
def include_file(ctx, name):
    env = ctx.environment
    return jinja2.Markup(env.loader.get_source(env, name)[0])


def main():
    loader = jinja2.FileSystemLoader(searchpath='.')
    env = jinja2.Environment(loader=loader)
    env.globals['include_file'] = include_file
    env.globals['version'] = strftime('%Y%m%d%H%M', gmtime())
    env.globals['timestamp'] = strftime('%d %b %Y %H:%M UTC', gmtime())
    filers = env.get_template('template.j2').render()
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'subscription.txt'), 'w', encoding='utf-8') as file:
        file.write(filers)


if __name__ == '__main__':
    main()
