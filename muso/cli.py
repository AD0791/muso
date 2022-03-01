from typer import (
    Typer,
    Exit,
    Option,
    echo
) 
from typing import Optional

from muso import(
  __app_name__, 
  __version__  
) 


app = Typer()






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


