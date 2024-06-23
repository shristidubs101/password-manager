# This is a useful utility script that can be used to encrypt/decrypt with AES-256 using pycryptodome library

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys

def encrypt(key, source, encode=True, keyType = 'hex'):
	source = source.encode()
	if keyType == "hex":
		 # Convert key (in hex representation) to bytes 
		key = bytes(bytearray.fromhex(key))

	IV = Random.new().read(AES.block_size)  # generate IV
	encryptor = AES.new(key, AES.MODE_CBC, IV)
	padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
	source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
	data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
	return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True,keyType="hex"):

	source = source.encode()
	if decode:
		source = base64.b64decode(source)

	if keyType == "hex":
		# Convert key to bytes
		key = bytes(bytearray.fromhex(key))
	

	IV = source[:AES.block_size]  # extract the IV from the beginning
	decryptor = AES.new(key, AES.MODE_CBC, IV)
	data = decryptor.decrypt(source[AES.block_size:])  # decrypt
	padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
	if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
		raise ValueError("Invalid padding...")
	return data[:-padding]  # remove the padding



if __name__ == "__main__":
	op = sys.argv[1]
	if op=="encrypt" or op==1:
		msg = sys.argv[2]
		key = sys.argv[3]
		keyType = sys.argv[4]
		cipher = encrypt(key,msg,keyType=keyType)
		print(cipher)
	elif op=="decrypt" or op==2:
		cipher = sys.argv[2]
		key = sys.argv[3]
		keyType = sys.argv[4]
		msg = decrypt(key,cipher,keyType=keyType)
		print(msg)