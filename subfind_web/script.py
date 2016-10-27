from os.path import abspath
from os.path import dirname

import click


@click.command()
@click.option('--port', '-p', default=5000, help='Web port')
@click.option('--dev', is_flag=True, help='Run in development mode')
def run(port, dev):
    from tb_api.script import start
    web_dir = abspath(dirname(__file__))
    start(
        base_name='subfind_web.service',
        module_suffix='Service',
        project_dir=web_dir,
        debug=dev,
        port=port
    )

