from muso.utils import df_to_table 
from rich import box




def table_helper(data,tab,index=False):
    table = df_to_table(data, tab,show_index=index)
    table.row_styles = ["none", "dim"]
    table.box = box.SIMPLE_HEAD
    return table

