import click

from subfind_web.app import start_web


@click.command()
@click.option('--port', '-p', default=32500, help='Web port')
@click.option('--dev', is_flag=True, help='Run in development mode')
def run(port, dev):
    print('run111')
    start_web(port=port, debug=dev)


if __name__ == '__main__':
    run()
