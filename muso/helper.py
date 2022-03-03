from muso.utils import df_to_table 
from rich import box
from rich.columns import Columns
from rich.panel import Panel



def table_helper(data,tab,index=False):
    table = df_to_table(data, tab,show_index=index)
    table.row_styles = ["none", "dim"]
    table.box = box.HEAVY 
    return table


def resume_helper(df1,df2,tab,index=False):
    table = df_to_table(df1, tab,show_index=index)
    table2 = df_to_table(df1, tab,show_index=index)
    
    table.row_styles = ["none", "dim"]
    table.box = box.HEAVY 
    table2.row_styles = ["none", "dim"]
    table2.box = box.HEAVY 
    
    panel_element = [table,table2]
    tables = [Panel(tabs,box=box.HEAVY) for tabs in panel_element]
    cols = Columns(tables)
    return cols    
    