import mysql.connector as mysqltr
from rich import print as printc
from rich.console import Console
console=Console()

def dbconfig():
    try:
        db = mysqltr.connect(
            host="localhost",
            user="root",
            passwd="demo"
        )
    except Exception as e:
        console.print_exception(show_locals=True)
    
    return db
