from os.path import abspath, join
from os.path import dirname

import click
from tb_api.loader.ioc import LoaderIOC
from tb_api.model.config import Config


@click.command()
@click.option('--port', '-p', default=32500, help='Web port')
@click.option('--dev', is_flag=True, help='Run in development mode')
def run(port, dev):
    from tb_api.script import start
    web_dir = abspath(dirname(__file__))

    project_dir = join(web_dir, 'ui/build')
    config = Config(project_dir, debug=dev, port=port)
    config_files = [join(web_dir, 'conf/api.yml')]
    config.loader = LoaderIOC(config_files, module_suffix='Service')

    start(
        config
    )

