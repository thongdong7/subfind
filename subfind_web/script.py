import click

from subfind_web.app import start_web


@click.command()
@click.option('--port', '-p', default=32500, help='Web port')
@click.option('--dev', is_flag=True, help='Run in development mode')
def run(port, dev):
    # from tb_api.script import start
    # web_dir = abspath(dirname(__file__))
    #
    # project_dir = join(web_dir, 'ui/build')
    # config = Config(project_dir, debug=dev, port=port)
    # config_files = [join(web_dir, 'conf/api.yml')]
    # config.loader = LoaderIOC(config_files, module_suffix='Service')
    #
    # start(
    #     config
    # )

    start_web(port=port, debug=dev)


if __name__ == '__main__':
    run()
