#! /home/daim/plebdev/developing-cln-plugins/venv/bin/python
from pyln.client import Plugin

plugin = Plugin()

# @plugin.init()
# def init(options, configuration, plugin):
#     plugin.log("Plugin helloworld.py initialized")

@plugin.method("myplugin-test")
def myplugin(plugin, foo="bar"):
    """This method tests the plugin"""
    return {"message": "This plugin works!. The option you specified is: {}".format(foo)}

@plugin.subscribe("block_added")
def on_connect(plugin, block, **kwargs):
  plugin.log("event rcieved: {}".format(block))
  return

plugin.run()

