from rich import box
from rich.columns import Columns
from rich.panel import Panel
from pandas import DataFrame
from typer import echo

from musoapp import (
    __app_name__,
    __version__
)
from musoapp.utils import df_to_table 


def _version_callback(value: bool) -> None:
    if value:
        echo(f"{__app_name__} v{__version__}")
        raise Exit()



def table_helper(data,tab,index=False):
    table = df_to_table(data, tab,show_index=index)
    table.row_styles = ["none", "dim"]
    table.box = box.HEAVY 
    return table


def resume_helper(df1,df2,tab,index=False):
    table = df_to_table(df1, tab,show_index=index)
    table2 = df_to_table(df2, tab,show_index=index)
    
    table.row_styles = ["none", "dim"]
    table.box = box.HEAVY 
    table2.row_styles = ["none", "dim"]
    table2.box = box.HEAVY 
    
    panel_element = [table,table2]
    tables = [Panel(tabs,box=box.HEAVY) for tabs in panel_element]
    cols = Columns(tables)
    return cols


def count_helper(bd,ibd,tab,index=False):
    df = DataFrame(
        {
            "beneficiaires directs":[bd.case_id.count()],
            "beneficiaires indirects":[ibd.ib_case_id.count()]
        }
    )
    
    table = df_to_table(df, tab,show_index=index)
    table.row_styles = ["none", "dim"]
    table.box = box.HEAVY 
    
    return table
    