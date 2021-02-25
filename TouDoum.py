import click
import os

from dotenv import load_dotenv

from core.Config import Config
from core.Client import Client
from core.Server import Server
from core.manager.PluginManager import PluginManager
from core.manager.DataDriverManager import DataDriverManager
from core.lib import console


@click.group()
def cli_config():
    pass


@click.group()
def cli_run():
    pass


cli = click.CommandCollection(sources=[cli_config, cli_run])


@cli_config.command()
@click.option('--data-driver', '-dd', 'data_driver', help="Give a driver name to setup")
def config(data_driver: str):
    """
        Setup data driver for ip storage
        todo
    """
    if data_driver is None:
        ddm = DataDriverManager()
        ddm.print_available_drivers()
    else:
        ddm = DataDriverManager(data_driver)
        driver = ddm.get_driver()
        driver.configure()


@cli_run.command()
@click.option('--plugin-list', 'plugin_list', is_flag=True, help="List all plugins available")
@click.option('--plugins', help="Give plugin list separated by ',' use '-' for select all plugin")
def run(plugin_list: bool, plugins: str):
    """
        Version 3.0 work in progress
    """

    config = Config()

    if plugin_list:
        pluginManager = PluginManager()
        pluginManager.print_plugins_list()
        exit(0)

    if plugins is not None:
        plugins = PluginManager(plugins)
        print("Loaded : {0} plugins".format(plugins.plugin_loaded()))

        # todo load data dataDriver file.json or mongo

        # check if app running in docker environment and run server or client code
        if config.docker_mode:
            if os.environ.get("IS_SERVER"):
                # run server mode
                server = Server()
            else:
                # run client mode
                client = Client()
        exit(0)

    print("No arg detected :/")
    print("Please run 'python3 Toudoum.py run --help'")


if __name__ == '__main__':
    click.clear()
    console.banner()
    load_dotenv(".env")
    if os.environ.get("APP_VERSION") is None:
        print("Error no environments file found :/")
        exit(1)

    if os.getuid() == 0:  # todo patch here for check windows admin
        config = Config()
        config.load()
        cli()
    else:
        console.error("You need to be run this script with root privileges")
        exit(1)