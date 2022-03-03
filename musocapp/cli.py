from typer import (
    Typer,
    Exit,
    Option,
    echo
) 
from typing import Optional
from rich.table import Table
from rich.console import Console
from musocapp.helper import(
    table_helper,
    resume_helper,
    _version_callback,
    count_helper
) 
from musocapp import(
  __bd,
  __ibd,
  _bd,
  _ibd 
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
    
    
@app.command(short_help="Tableau donnant le count des beneficiaires")
def count():
    count_tab = count_helper(_bd, _ibd, _table)
    _console.print(count_tab)    
    


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

