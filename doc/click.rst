.. _click_cli:

Command-Line with `click`
=========================

click_ is another popular package for creating beautiful CLI.

.. _click: http://click.pocoo.org

One option to use `trafaret_config` is to define new `click` argument type based, which expects path
to an existing configuration file plus trafaret rules.

Create `cli.py`:

.. code-block:: python
    :linenos:

    import click
    import trafaret_config as traf_cfg
    import trafaret as t
    import time

    CONFIG_TRAFARET = t.Dict({t.Key("host"): t.String(), t.Key("port"): t.Int()})


    class TrafaretYaml(click.Path):
        """Configuration read from YAML file checked against trafaret rules."""
        name = "trafaret yaml file"

        def __init__(self, trafaret):
            self.trafaret = trafaret
            super().__init__(
                exists=True, file_okay=True, dir_okay=False, readable=True)

        def convert(self, value, param, ctx):
            cfg_file = super().convert(value, param, ctx)
            try:
                return traf_cfg.read_and_validate(cfg_file, self.trafaret)
            except traf_cfg.ConfigError as e:
                msg = "\n".join(str(err) for err in e.errors)
                self.fail("\n" + msg)


    @click.group()
    def cli():
        pass


    @cli.command()
    @click.argument("config", type=TrafaretYaml(CONFIG_TRAFARET))
    def validate(config):
        """Validate configuration file structure."""
        click.echo("OK: Configuration is valid.")


    @cli.command()
    @click.argument("config", type=TrafaretYaml(CONFIG_TRAFARET))
    def run(config):
        """Run web application.
        """
        # Start the application
        host = config["host"]
        port = config["port"]
        print("Would like to run the app at {host}:{port}...".format(
            host=host, port=port))
        time.sleep(5)
        print("..done.")


    if __name__ == "__main__":
        cli()


`CONFIG_TRAFARET` is sample trafaret rule for our config file, which may look like `config.yaml`::

    host: localhost
    port: 1234


`class TrafaretYaml(click.Path)` defines a class for new `click` type.


`def cli():` defines top level command to run and it has two subcommands:


Subcommand validating the configuration file is really simple::

    @cli.command()
    @click.argument("config", type=TrafaretYaml(CONFIG_TRAFARET))
    def validate(config):
        """Validate configuration file structure."""
        click.echo("OK: Configuration is valid.")

using `type=TrafaretYaml` it implicitly expects path to config file and at the same time prescribes
trafaret rules for it's content.

`def run():` goes one step further and uses the configuration values.


Sample usage
------------

First explore the main command::

    $ python cli.py
    Usage: cli.py [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    run       Run web application.
    validate  Validate configuration file structure.

It provides two subcommands.

Subcommand `validate` allows configuration file validation::

    $ python cli.py validate cfg.yaml
    OK: Configuration is valid.

If the config file does not exist::

    $ python cli.py run cfg-not-here.yaml
    Usage: cli.py run [OPTIONS] CONFIG

    Error: Invalid value for "config": Path "cfg-not-here.yaml" does not exist.

it reports this problem.

If port number has value `1234a`, it uses trafaret rules to report the problem::

    $ python cli.py va lidate cfg.yaml
    Usage: cli.py validate [OPTIONS] CONFIG

    Error: Invalid value for "config":
    cfg.yaml:2: port: value can't be converted to int

If all is fine, it allows running the applicaiton::

    $ python cli.py run cfg.yaml
    Would like to run the app at localhost:1234...
    ..done.

Hint: add subcommand `init` printing sample configuration file content.
