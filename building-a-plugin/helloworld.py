#! /home/daim/plebdev/developing-cln-plugins/venv/bin/python

from pyln.client import Plugin

plugin = Plugin();

plugin.init()

@plugin.method("hello")
def hello(plugin, name="world"):
    """This method says hello"""
    return {"message": "Hello {}".format(name)}

plugin.run()


