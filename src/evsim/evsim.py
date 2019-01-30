import click
from datetime import datetime
import logging
import os

from evsim import simulation
from evsim.data import loader


@click.group(name="evsim")
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug

    os.makedirs("./logs", exist_ok=True)
    fh = logging.FileHandler(
        "./logs/%s.log" % str(datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    fh.setFormatter(logging.Formatter("%(name)-10s: %(levelname)-7s %(message)s"))
    fh.setLevel(logging.DEBUG)
    ctx.obj["FH"] = fh

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(levelname)-8s: %(message)s"))
    if not debug:
        sh.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.DEBUG, datefmt="%d.%m. %H:%M:%S", handlers=[sh, fh]
    )


@cli.command(help="Start the EV Simulation.")
@click.pass_context
@click.option(
    "-n",
    "--name",
    default=str(datetime.now().strftime("%Y%m%d-%H%M%S")),
    help="Name of the Simulation.",
)
@click.option(
    "-c", "--ev-capacity", default=17.6, help="Battery capacity of EV in kWh."
)
@click.option(
    "-s",
    "--charging-speed",
    default=3.6,
    help="Charging power of charging stations in kW.",
)
@click.option(
    "--max-ev-range", default=160, help="Maximal range in km of EV when fully charged."
)
def simulate(ctx, name, ev_capacity, charging_speed, max_ev_range):
    click.echo("Debug is %s" % (ctx.obj["DEBUG"] and "on" or "off"))
    simulation.start(name, ev_capacity, charging_speed, max_ev_range)


@cli.group(invoke_without_command=True, help="(Re)build all data sources.")
@click.pass_context
def build(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Building all data sources.")
        loader.rebuild()


@build.command(help="(Re)build car2go trip data.")
@click.pass_context
def trips(ctx):
    click.echo("Building car2go trip data...")
    loader.load_car2go_trips(rebuild=True)


@build.command(help="(Re)build mobility demand data.")
@click.pass_context
def mobility_demand(ctx):
    click.echo("Building mobility demand data...")
    loader.load_car2go_capacity(rebuild=True)


@build.command(help="(Re)build intraday price data.")
@click.pass_context
def intraday_prices(ctx):
    click.echo("Rebuilding intraday price data...")
    loader.load_intraday_prices(rebuild=True)


@build.command(help="(Re)build balancing price data.")
@click.pass_context
def balancing_prices(ctx):
    click.echo("Rebuilding balanacing price data...")
    loader.load_balancing_data(rebuild=True)
