from typer import (
    Typer,
    Exit,
    Option,
    echo
) 
from typing import Optional
from rich import box
from rich.table import Table
from rich.console import Console
from muso import(
  __app_name__, 
  __version__,
  __bd,
  __ibd 
)
from muso.utils import df_to_table 

app = Typer()
_console = Console()
_table = Table(show_header=True, header_style="bold magenta")

@app.command(short_help="Tableau des beneficaires direct de MUSO")
def bdirect():
    table = df_to_table(__bd, _table,show_index=False)
    table.row_styles = ["none", "dim"]
    table.box = box.SIMPLE_HEAD
    _console.print(table)

@app.command(short_help="Tableau des beneficaires indirect de MUSO")
def bindirect():
    table = df_to_table(__ibd, _table,show_index=False)
    table.row_styles = ["none", "dim"]
    table.box = box.SIMPLE_HEAD
    _console.print(_table)


def _version_callback(value: bool) -> None:
    if value:
        echo(f"{__app_name__} v{__version__}")
        raise Exit()


@app.callback()
def main(
    version: Optional[bool] = Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


