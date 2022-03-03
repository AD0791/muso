from typer import (
    Typer,
    Exit,
    Option,
    echo
) 
from typing import Optional
from rich.table import Table
from rich.console import Console
from muso.helper import(
    table_helper,
    resume_helper
) 
from muso import(
  __app_name__, 
  __version__,
  __bd,
  __ibd 
)

app = Typer()
_console = Console()
_table = Table(show_header=True, header_style="bold magenta")

@app.command(short_help="Tableau des beneficaires direct de MUSO")
def bdirect():
    table = table_helper(__bd, _table)
    _console.print(table)

@app.command(short_help="Tableau des beneficaires indirect de MUSO")
def bindirect():
    table = table_helper(__ibd, _table)
    _console.print(table)
    
    
@app.command(short_help="Les tableaux des beneficiaires directs et indirects")
def resume():
    res = resume_helper(__bd, __ibd, _table)
    _console.print(res)


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

