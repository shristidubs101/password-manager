from dbconfig import dbconfig
import aesutil

from rich import print as printc

from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

def computerMasterKey(mp,ds):
    password=mp.encode()
    salt=ds.encode()
    key=PBKDF2(password,salt,32,count=1000000,hmac_hash_module=SHA512)
    return key
    
    

def add_entry(mp, ds, sitename, siteurl, email, username):
    # get password
    password = getpass("Password:")
    
    mk=computerMasterKey()
    encrypted=aesutil.encrypt(key=mk,source=password,keyType="bytes")
    
    #add to db
    db=dbconfig()
    cursor=db.cursor()
    query = """INSERT INTO Password_Manager.entries( sitename, siteurl, email, username, password)values(%s,%s,%s,%s,%s)"""
    val=( sitename, siteurl, email, username, encrypted)
    cursor.execute(query,val)
    db.commit()
    
    printc("[green][+][/green] Added Entry.")
