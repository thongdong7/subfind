import logging
from pprint import pprint
from time import time

import click
import os
import yaml
from jinja2 import Template
from os.path import join, dirname, exists, relpath
from watchdog.events import FileSystemEventHandler


def load_config():
    return yaml.load(open('gen/config.yml'))


@click.command(help='Generate css import')
def gen_css():
    start = time()
    current_folder = os.path.abspath(os.path.dirname(__file__))
    project_dir = current_folder

    gen_dir = join(current_folder, 'gen')
    # generated_dir = join(current_folder, 'generated')
    generated_dir = current_folder

    config = load_config()

    template_dir = join(gen_dir, 'templates')
    for root_dir, child_dirs, file_names in os.walk(template_dir):
        for file_name in file_names:
            file_path = join(root_dir, file_name)

            relative_path = relpath(file_path, template_dir)
            # print(relative_path)

            output_path = join(project_dir, relative_path)
            output_dir = dirname(output_path)
            if not exists(output_dir):
                os.makedirs(output_dir)

            template = Template(open(file_path).read())
            content = template.render(**config)

            open(output_path, 'w').write(content)

    templates = config.get('template', [])
    if templates:
        for template_config in templates:
            path = join(gen_dir, 'templates', template_config['path'])
            template = Template(open(path).read())
            content = template.render(**config)
            output_path = join(generated_dir, template_config['path'])
            output_dir = dirname(output_path)
            if not exists(output_dir):
                os.makedirs(output_dir)

            print(output_path)
            open(output_path, 'w').write(content)

    print('Generated completed in %s seconds' % (time() - start))


@click.command()
def gen_listener():
    import sys
    import time
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler



    class GenFileSystemEventHandler(FileSystemEventHandler):
        def __init__(self):
            self.watch_files = set()
            self.watch_dir = set()

        # def on_any_event(self, event):
        #     super().on_any_event(event)
        #
        #     pprint(event)
        #     # if event.src_path in self.watch_files:
        #     #     print(event.src_path)
        #     #     match = False
        #     # else:
        #     #     for watch_dir in self.watch_dir:
        #     #         if event.src_path.startswith(watch_dir):
        #     #             match = True
        #     #             break
        #     print('Gen')
        #     gen_css()

        def on_modified(self, event):
            super().on_modified(event)
            print('modified')
            gen_css()

        def on_deleted(self, event):
            super().on_deleted(event)

            print('on deleted')
            gen_css()

    event_handler = GenFileSystemEventHandler()

    gen_dir = join(dirname(__file__), 'gen')
    template_dir = join(gen_dir, 'templates')
    config_file = join(gen_dir, 'config.yml')

    event_handler.watch_files.add(config_file)
    event_handler.watch_dir.add(template_dir)

    observer = Observer()
    observer.schedule(event_handler, gen_dir, recursive=True)
    # observer.schedule(event_handler, config_file)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    gen_css()
    # gen_listener()
