import pwinput
import hashlib
import sys
import pyperclip

from rich import print as printc

import config
import add
import retrieve
import generate
from dbconfig import dbconfig

from rich.console import Console

console = Console()

def inputAndValidateMasterPassword():
	mp = pwinput.pwinput(prompt="Choose a MASTER PASSWORD: ", mask="*")
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

#####################################################
def enter_data():
    res = inputAndValidateMasterPassword()
    if res is not None:
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
        add.add_entry(res[0],res[1], name, url, email, login)
    else:
        printc("[red]Next time Bitch ![/red]")
                
###################################### 

def extract():
    res = inputAndValidateMasterPassword()
    if res != None:
        search = {}
        
        name = input("Enter the site name (-s): ")
        url = input("Enter the site URL (-u): ")
        email = input("Enter the email (-e): ")
        login = input("Enter the username (-l): ")
        copy=input("Do you want to copy the password [yes,no]? ").lower()
        
        if copy =="yes":
            decryptPassword=True
        else:
            decryptPassword=False
        
        if res is not None:
            retrieve.retrieveEntries(res[0],res[1],search,decryptPassword)
        
    else:
        printc("[bold magenta]Try next time bbg <3 ![/bold magenta]")
        
#################################################

def generate_pass():
    res = inputAndValidateMasterPassword()
    if res != None:
        
        while True:
            length=input("Enter the length of the password to be generated:")
            if length == "":
                printc("[red][+][/red] Specify length of the password to generate.")
                continue
            else:
                password = generate.GeneratePassword(length)
                pyperclip.copy(password)
                printc("[green][+][/green] Password generated and copied to clipboard")
                break
                
    else:
        printc("[bold magenta]Try next time bbg <3 ![/bold magenta]")

###################################################

def main():
    while True:
        option = input("OPTIONS:\n (a)Add\n (b)Extract\n (c)Generate\n (d)Exit \nEnter your choice: ").lower()
        if option in ["add","a"]:
            enter_data()
            
            
        elif option in ["extract","b"]:
            extract()
                
                
        elif option in ["generate","c"]:
            generate_pass()
        
        elif option in ["exit","d"]:
            printc("[yellow] Exiting the program![/yellow]")
            quit()
        
        else:
            print("[red]Invalid option[/red]")
            continue
                
        
print("*"*30," Welcome To Password Manager ","*"*30)
main()