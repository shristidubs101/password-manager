from getpass import getpass
import hashlib
import pyperclip

from rich import print as printc

import config
import add
import retrieve
import generate
from dbconfig import dbconfig


def inputAndValidateMasterPassword():
	mp = getpass("MASTER PASSWORD: ")
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT * FROM Password_Manager.classified"
	cursor.execute(query)
	result = cursor.fetchall()[0]
	if hashed_mp != result[0]:
		printc("[red][!] WRONG! [/red]")
		return None

	return [mp,result[1]]


def enter_data():
    name = input("Enter the site name (-s): ")
    url = input("Enter the site URL (-u): ")
    email = input("Enter the email (-e): ")
    login = input("Enter the username (-l): ")
    length = input("Enter the desired password length (--length): ")
        
    try:
        length = int(length)
    except ValueError:
        length = None
        
    if name == "" or url == "" or login == "":
            if name == "":
                printc("[red][!][/red] Site Name (-s) required ")
            if url == "":
                printc("[red][!][/red] Site URL (-u) required ")
            if login == "":
                printc("[red][!][/red] Site Login (-l) required ")
                return
            
    if email == "":
        email = ""
            
    res = inputAndValidateMasterPassword()
    if res is not None:
        add.add_entry(res[0],res[1], name, url, email, login)
        
def extract():
    pass


def generate():
    pass

def main():
    option = input("Enter an option (a)Add / (b)Extract / (c)Generate: ").lower()
    if option in ["add","a"]:
        enter_data()
        
        
    """if option in ["extract","e"]:
        res = inputAndValidateMasterPassword()
        search = {}
        if name != "":
            search["sitename"] = name
        if url != "":
            search["siteurl"] = url
        if email != "":
            search["email"] = email
            if login != "":
                search["username"] = login
                
        if res != "":
            retrieve.retrieveEntries(res[0],res[1],search,decryptPassword = args.copy)
            
            
    if option in ["generate","g"]:
        if length == "":
            printc("[red][+][/red] Specify length of the password to generate (--length)")
            return
        password = generate.generatePassword(length)
        pyperclip.copy(password)
        printc("[green][+][/green] Password generated and copied to clipboard")"""
        
        
print("*"*30," Welcome To Password Manager ","*"*30)

res = inputAndValidateMasterPassword()
if res==None:
    printc("[green][!] Better luck next time! [/green]")
else:
    main()