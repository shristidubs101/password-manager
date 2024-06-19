import argparse

parser=argparse.ArgumentParser(description="Description")

parser.add_argument('option',help='1.Add/2.Extract/3.Generate')
parser.add_argument("-s","--name",help="Site name")
parser.add_argument("-u","--url",help="Site URL")
parser.add_argument("-e","email",help="Email")
parser.add_argument("-l","login",help="Username")
parser.add_argument("--length",help="Length of the password to generate",type=int)
parser.add_argument("-c","--copy",action='store_true',help='Copy password to clipboard')

args=parser.parse_args()