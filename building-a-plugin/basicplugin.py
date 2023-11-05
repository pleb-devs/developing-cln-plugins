#! /home/daim/plebdev/developing-cln-plugins/venv/bin/python


# copied from https://lnroom.live/2023-03-28-live-0001-understand-cln-plugin-mechanism-with-a-python-example/

import sys
import os
import json
import socket

myplugin_out="/tmp/plugin_out"
if os.path.isfile(myplugin_out):
    os.remove(myplugin_out)
def printout(s):
    with open(myplugin_out, "a") as output:
        output.write(s)

# getmanifest
request = sys.stdin.readline()
sys.stdin.readline() # "\n"

printout("GETMANIFEST\n")
printout(request)
printout("\n==================================================\n\n")

req_id = json.loads(request)["id"]

manifest = {
    "jsonrpc": "2.0",
    "id": req_id,
    "result": {
        "dynamic": True,
        "options": [{
            "name": "foo_opt",
            "type": "string",
            "default": "bar",
            "description": "description"
        }],
        "rpcmethods": [{
            "name": "myplugin",
            "usage": "",
            "description": "description"
        }]
    }
}

sys.stdout.write(json.dumps(manifest))
sys.stdout.flush()

# init
request = sys.stdin.readline()
sys.stdin.readline() # "\n"

printout("INIT\n")
printout(request)
printout("\n==================================================\n\n")