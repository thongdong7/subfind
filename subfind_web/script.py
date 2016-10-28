from os.path import abspath, join
from os.path import dirname

import click


@click.command()
@click.option('--port', '-p', default=32500, help='Web port')
@click.option('--dev', is_flag=True, help='Run in development mode')
def run(port, dev):
    from tb_api.script import start
    web_dir = abspath(dirname(__file__))
    start(
        base_name='subfind_web.service',
        module_suffix='Service',
        project_dir=join(web_dir, 'ui/build'),
        debug=dev,
        port=port
    )

