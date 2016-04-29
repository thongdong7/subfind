import click
import os
import yaml
from jinja2 import Template
from os.path import join, dirname, exists


def load_config():
    return yaml.load(open('client/config.yml'))


@click.command(help='Generate css import')
def gen_css():
    current_folder = os.path.abspath(os.path.dirname(__file__))
    # generated_dir = join(current_folder, 'generated')
    generated_dir = current_folder

    config = load_config()
    templates = config.get('template', [])
    for template_config in templates:
        path = join(current_folder, 'templates', template_config['path'])
        template = Template(open(path).read())
        content = template.render(**config)
        output_path = join(generated_dir, template_config['path'])
        output_dir = dirname(output_path)
        if not exists(output_dir):
            os.makedirs(output_dir)

        open(output_path, 'w').write(content)

if __name__ == '__main__':
    gen_css()
