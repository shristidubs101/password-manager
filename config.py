from dbconfig import dbconfig

import pwinput
import hashlib
import sys

import string
import random

from rich import print as printc
from rich.console import Console

console = Console()


def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def config():
    # create a database
    db = dbconfig()
    cursor = db.cursor()

    try:
        database_name = "Password_Manager"
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        cursor.execute(create_database_query)

    except Exception as e:
        printc("[red][!]An error occured while creating database.")
        console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Database created")

    # create tables
    query = """CREATE TABLE IF NOT EXISTS Password_Manager.classified(masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"""
    cursor.execute(query)
    printc("[green][+][/green] Table 'classified' created")

    query = """CREATE TABLE IF NOT EXISTS Password_Manager.entries(sitename TEXT NOT NULL, siteurl TEXT NOT NULL,email TEXT,
        username TEXT, password TEXT NOT NULL)"""
    cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    query = """SELECT COUNT(1) FROM Password_Manager.classified"""
    cursor.execute(query)

    if cursor.fetchone() == (0,):
        mp = ""
        while 1:
            mp = pwinput.pwinput(prompt="Choose a MASTER PASSWORD: ", mask="*")
            if mp == pwinput.pwinput(prompt="Re-type: ", mask="*") and mp != "":
                break
            printc("[yellow][-]Please try again.[/yellow]")

        # Hash the master password
        hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
        printc("[green][+][/green] Generated hash of MASTER PASSWORD")

        # Generate a DEVICE SECRET
        ds = generateDeviceSecret()
        printc("[green][+][/green] Generated DEVICE SECRET")

        # Add them to db
        query = """INSERT INTO Password_Manager.classified(masterkey_hash,device_secret)values(%s,%s)"""
        val = (hashed_mp, ds)
        cursor.execute(query, val)
        db.commit()

        printc("[green][+][/green] Added to Database.")

    else:
        printc("[green]!MASTER PASSWORD already exists.[green]")

    printc("[green][+] Configuration Done![/green]")

    db.close()


config()
