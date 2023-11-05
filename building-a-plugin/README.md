# Building a CLN Plugin

Using the `pyln-client` library found [here](https://github.com/ElementsProject/lightning/tree/master/contrib/pyln-client)

## Introduction

I put a bit of a primer in [some slides](https://docs.google.com/presentation/d/1BwtTjP8ywGsT8BDt8QGOkgnoAKGiuDWk8-BbzlAu4SU/edit?usp=sharing), but these are not necessary.

Basically, we will be adding custom functionality to a c-lightning node using their plugin architecture. The [docs on plugins](https://docs.corelightning.org/docs/plugin-development) are helpful.

### Prerequisites

1. You will need a bitcoind backend and at least 2 c-lighnting nodes running that you are able to interact with. Check out [environment-setup](../environment-setup/) for instructions gettting your development environment good to go.

2. Python knowledge is helpful as we will be using a Python library

3. Knowledge of bitcoin and lightning like transactions, channels, and invoices

## Setup

Assuming you have bitcoind and at least 2 lightning nodes running, there are just a few things we will need to do before we can start building a plugin.

1. Activate a python virtual environment (not entirely necessary)

```
virtualenv venv #this create a venv directory
source ./venv/bin/activate #activate the venv
```

You'll know this worked if each new line on your terminal has `(venv)`

2. Install `pyln-client`

```
pip install pyln-client
```

Because we are using a virtual environment, the library will only be accessible from this virtual environment, but it also will not mess up anything with your global python.

3. Start your regtest environment

Use the [startup_regtest](./startup_regtest.sh) script (copied from [cln repo](https://github.com/ElementsProject/lightning/contrib/startup_regtest.sh)) to fire up some lightning nodes with a bitcoind backend.

```
source ./startup_regtest.sh # load all the functions
```

The above command will output something like:

```
lightning-cli is /usr/local/bin/lightning-cli
lightningd is /usr/local/bin/lightningd
Useful commands:
  start_ln 3: start three nodes, l1, l2, l3
  connect 1 2: connect l1 and l2
  fund_nodes: connect all nodes with channels, in a row
  stop_ln: shutdown
  destroy_ln: remove ln directories
```

Now, we can use the `start_ln` command which defaults to 2 lightning nodes, but accepts any number to specify the number of nodes to start. This will also start bitcoind in regtest mode.

```
start_ln # start 2 lightning nodes and 1 bitcoind
```

If this works, then the output should look like:

```
{
  "name": "default"
}
mkdir: created directory '/tmp/l1-regtest'
[1] 8568
mkdir: created directory '/tmp/l2-regtest'
[2] 8608
WARNING: eatmydata not found: install it for faster testing
Commands:
        l1-cli, l1-log,
        l2-cli, l2-log,
        bt-cli, stop_ln, fund_nodes
```

This creates aliases for each of the nodes. Inspect the aliases with:

```
alias l1-cli
```

Finally, to verify everything is running, try some CLI commands on each of the nodes:

```
l1-cli getinfo
```

```
bt-cli getblockchaininfo
```

Sweet! Now you should have all the dependencies installed.

## Starting a Plugin on Your Node

To test your plugin, you will need to start it on a node.

I created a [helloworld](./helloworld.py) plugin that you can use to test this.

There are a few options to start a plugin. Because we already have our nodes running we will use the `plugin start` command.

```
l1-cli plugin start /path/to/your/plugin.py
```

> > _NOTE_: Make sure the shebang (thats the `#!`) at the top of the plugin file points to python.

> > If you set up a virtual env as directed above you should find python in `./venv/bin/python`. You can check by running:

```
which python
```

This will output the path to your executable python. For me it's at `/home/daim/plebdev/developing-cln-plugins/venv/bin/python`.

Let's test this out!

Start the `helloworld` plugin on `l1`:

```
l1-cli plugin start $(pwd)/helloworld.py
```

Verify that the plugin is running with:

```
l1-cli plugin list
```

and you should see the plugin output like:

```
 {
    "name": "/home/daim/plebdev/developing-cln-plugins/building-a-plugin/helloworld.py",
    "active": true,
    "dynamic": true
 }
```

Now that this plugin is running you can run

```
l1-cli hello
```

which will output a message to the console.

## Restart Plugins

Whenever you make a change to the plugin you are developing, the plugin will need to be restarted for changes to take effect.

To do this, you will need to stop and start the plugin.

Stop the plugin with

```
l1-cli plugin stop helloworld.py
```

Then, start it again with

```
l1-cli plugin start $(pwd)/helloworld.py
```

### Auto Restart

This can get a bit annoying every time you make a change you have to run these two commands.

A script for that would be nice...

I made the [restart_plugin](./restart_plugin.sh) script to do just that.

**Make sure that you have the right path set in `PLUGIN_PATH` variable**

This script takes one optional argument to specify the node number you want to stop/start the plugin on. The default is `l1`

For example, restart the plugin on `l1`:

```
./restart_plugin.sh
```

Or, restart on `l2`:

```
./restart_plugin.sh 2
```

This is _sort of_ automatic. We can make it more automatic though!

You'll need to have `entr` installed. On Ubuntu, you can do this with:

```
sudo apt install entr
```

Now, in a separate terminal, we can watch for any changes to the plugin file and run the restart script whenever a file changes.

Open a new terminal, `cd` into your working directory and run:

```
ls | entr -s './restart_plugin.sh'
```

Try changing then saving `helloworld.py`, and you should see more output in the console that you ran the above command.

## Inspecting `getmanifest` and `getinfo`

Alright, that was a lot, but now we have everything we need! Let's just check out the `getmanifest` and `getinfo` requests that get sent by the node to the plugin. If you want to read more about these, check out [A Day in the Life of a Plugin](https://docs.corelightning.org/docs/a-day-in-the-life-of-a-plugin).

Another great resource in [lnroom.live](https://lnroom.live). Tony Aldon has a ton of videos going more in-depth on building plugins, but the one related to this is [here](https://lnroom.live/2023-03-28-live-0001-understand-cln-plugin-mechanism-with-a-python-example/)

I will go into a bit more detail in the live stream, but if you want to explore more I highly recommend Tony's video linked above.

I copied Tony's code from that video and added some extra print statements.

Let's change the `PLUGIN_PATH` to `basicplugin.py` which is a plugin that's NOT using `pyln-client`.

Now, the `basicplugin.py` should get started on `l1`. In this plugin, there is a `printout` function that will print anything we want to `/tmp/plugin_out`.

Inspect the output with:

```
cat /tmp/plugin_out
```

You can also run in a separate terminal

```
watch -n 1 cat /tmp/plugin_out
```

which will `cat` that file whenever it changes.

Take a look at [basicplugin.py](./basicplugin.py) to see what's going on, but this is as much as I'll say because, again, Tony does a great job covering this if you want to learn more.

## Using `pyln-client`

Finally! This is what we've all been waiting for. The `pyln-client` library abstracts everything that is happening in `basicplugin.py` into a few simple functions.

1. Import the library (**make sure you set the path to your python**)

```
#! /path/to/python

from pyln.client import Plugin
```

2. Create a new plugin instance

```
#! /path/to/python

from pyln.client import Plugin

plugin = Plugin()
```

3. Run the plugin

```
#! /path/to/python

from pyln.client import Plugin

plugin = Plugin()

plugin.init()

plugin.run()
```

That's all you need to initialize a plugin using `pyln-client`, but we want this to actually do something!

### Adding a Method

4. Add a method using a python decorator

```
#! /home/daim/plebdev/developing-cln-plugins/venv/bin/python
from pyln.client import Plugin

plugin = Plugin()

plugin.init()

@plugin.method("myplugin-test")
def myplugin_test(plugin, foo="bar"):
    """This method says hello"""
    return {"message": "This plugin works!. The option you specified is: {}".format(foo)}

plugin.run()
```

In python, you can use the `@` to "decorate" a function with another function. In this context, we used the `plugin.method` function to set the name of our method to `myplugin-test`. We placed this decorator right above the function that we want to execute when `myplugin-test` is run, so now whenever you run something like `l1-cli myplugin-test`, the myplugin_test function will be executed.

The syntax is a little weird, but just know that whatever you pass to `@plugin.method` will be the name of your method, and the function defined below that decorator is the function that will be executed whenever that method is used.

### Subscribe to Events

In the plugin docs, you'll find [different events](https://docs.corelightning.org/docs/event-notifications) that your plugin can subscribe to.

In the spirit of keeping it simple, we will subscribe to the [block_added](https://docs.corelightning.org/docs/event-notifications) event, but there is a ton to pick from depending on your needs.

5. Use a decorator to add a subscription

```
#! /home/daim/plebdev/developing-cln-plugins/venv/bin/python
from pyln.client import Plugin

plugin = Plugin()

@plugin.method("myplugin-test")
def myplugin_test(plugin, foo="bar"):
    """This method says hello"""
    return {"message": "This plugin works!. The option you specified is: {}".format(foo)}

@plugin.subscribe("block_added")
def on_connect(plugin, block, **kwargs):
  plugin.log("Block recieved: {}".format(block))
  return

plugin.run()
```

Mine a block:

```
bt-cli -generate 1
```

Check the node's logs:

```
l1-log | grep myplugin | tail
```

If it worked, you should see an output in your node's logs with the block hash and height of the block you just mined.

**Final Note:** I was having a hard time figuring out what _exactly_ needs to be passed to the decorated functions and could not find any clear answers in the code. If you get `TypeError`s it might be because you did not name the parameter correctly.

Send us a message in the [Discord](https://discord.gg/fpExywWpdA) if you need help with _any_ of this stuff!!

Happy coding :)
