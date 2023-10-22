# Setting Up A CLN Dev Environment

> **Livestreaming Sunday October, 22 @ 1pm PT -- 3pm CT -- 4pm ET**

- [Introduction](#introduction)
- [Instructions](#instructions)
- [Installing Bitcoin Core](#installing-bitcoin-core)
- [Installing CLN](#installing-cln)
- [Configuring Bitcoin Core](#bitcoin-config)
- [Learn bitcoin-cli](#bitcoin-cli)
- [Learn lightning-cli](#lightning-cli)


## Introduction

Getting everything properly installed and running on a development machine is frustrating for me, so I hope these docs are clear and helpful in getting you on your way to building CLN plugins.

C-Lightning has a plugin architecture that allows plebs to write custom code, and run it on their node using any programming language.

Before we can start writing code, we will need to set up a test environment consisting of 1 `bitcoind` instance and multiple `lightningd` instances. These nodes will all be running locally on your development machine.

In this workshop we will be building CLN from source and installing Bitcoin Core using `snapd`.

Final notes before getting into it:

> _These instructions are based on Ubuntu 22.04. Ask for help if you have trouble_
>
> This is a trimmed-down version of the CLN [install docs](https://github.com/ElementsProject/lightning/blob/master/doc/getting-started/getting-started/installation.md)

## Instructions

Copy the commands into your bash terminal. If you're on *Ubuntu 22.04* this should build smoothly, but different OSes will have different results. Usually copy & pasting your error into Chat-GPT/Google will help you find the missing packages.

The end **goal** is to have some nodes built and running on your local machine for convenient plugin development.

*I'll try to leave helpful comments in the install commands, so don't just blindly copy and paste.*

### Steps

1. [Install Bitcoin Core](#installing-bitcoin-core)
2. [Install CLN](#installing-cln)
   - [Get Dependencies](#dependencies)
   - [Clone](#clone)
   - [Activate Virtual Environment](#activate-venv)
   - [Get Python Dependencies](#python-dependencies)
   - [Configure CLN](#configure-cln)
   - [Make](#make)
4. [Configure Bitcoin Core](#bitcoin-config)
5. [Start Everything Up!](#start-your-nodes)
6. [Learn bitcoin-cli](#bitcoin-cli)
7. [Learn lightning-cli](#lightning-cli)

## Installing Bitcoin Core

We will just use snapd because its much simpler, but if you haven't yet it's worth it to try building Bitcoin Core from source.

```
sudo apt-get install snapd #install the snap package manager
sudo snap install bitcoin-core # use snap to install the `bitcoin-core` package
# Snap does some weird things with binary names; you'll
# want to add a link to them so everything works as expected
sudo ln -s /snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/
```

## Installing CLN

This is the fun part where we build CLN and hope it runs.

Install all packages you will need:

### Dependencies

```
sudo apt-get update #update apt package manager
sudo apt-get install -y \ #install the following packages and say 'yes' to everything
  autoconf automake build-essential git libtool libsqlite3-dev \
  python3 python3-pip net-tools zlib1g-dev libsodium-dev gettext libgmp-dev
```

### Clone

```
git clone https://github.com/ElementsProject/lightning.git
cd lightning
```

### Checkout release branch

```
git checkout v22.11.1
```

### Activate venv

This bumps you into a virtual python environment where anything you install won't affect the global state of python.

```
sudo apt install python3-virtualenv #install the virtualenv package
virtualenv venv #create a venv in current directory
source venv/bin/activate #activate the venv script
```

### Python Dependencies

```
pip3 install --upgrade pip
sudo pip3 install mako
```

### Configure CLN

Here you can specify any configuration flag you want before building. Refer to [cln docs](https://docs.corelightning.org/docs/configuration)

```
./configure
```

### Make

Run the [Makefile](https://github.com/ElementsProject/lightning/blob/master/Makefile) script and install

```
make
sudo make install
```

## Bitcoin Config

Now you should have `bitcoind` and `lightningd` in your PATH

Run `bitcoind -regtest` to start and create `~/.bitcoin`;

Now you can kill bitcoind with `CTRL + C`

There should be a `.bitcoin` in your home directory now. If you can't see it and you're on Linux try `ls -la`

```
cd ~/.bitcoin
touch bitcoin.conf #create a configuration file
```

Copy the following into your newly created file:

```
# anytime you start bitcoind it will automatically go to regtest
regtest=1
```
## Start Your nodes

You should now be able to start a bitcoin node and as many lightning nodes as you want.

Start bitcoind with the following command:

```
bitcoind -daemon
```

Stop bitcoin:

```
bitcoin-cli stop
```

### startup_regtest.sh

For simplicity, we will use this [handy script](https://github.com/ElementsProject/lightning/blob/master/contrib/startup_regtest.sh) provided in the CLN repo.

To use it, we first run from within the `lightning` directory that we cloned:

```
source ./contrib/startup_regtest.sh
```

This will create some functions for us to use. One of them is `start_ln`

Start 2 lightning nodes:
```
start_ln 2
```

**NOTE: ** If you get an error about you wallet, you may need to create a new wallet. That can be done with `bitcoin-cli createwallet "default"`

Now to verify that the nodes are running use the `getinfo` RPC method

```
l1-cli getinfo
```

If it's running you should see an output like:

```
{
   "id": "038b6f8e52dc4f275d316a345e1d70566b2c1fa0f972e5eb816c0faeda69513a14",
   "alias": "JUNIORFARM",
   "color": "038b6f",
   "num_peers": 1,
   "num_pending_channels": 0,
   "num_active_channels": 1,
   "num_inactive_channels": 0,
   "address": [],
   "binding": [
      {
         "type": "ipv4",
         "address": "127.0.0.1",
         "port": 7272
      }
   ],
   "version": "v22.11.1",
   "blockheight": 240,
   "network": "regtest",
   "fees_collected_msat": 0,
   "lightning-dir": "/tmp/l2-regtest/regtest",
   "our_features": {
      "init": "08a000080269a2",
      "node": "88a000080269a2",
      "channel": "",
      "invoice": "02000000024100"
   }
}
```


## Bitcoin-CLI

Here are some bitcoind commands to mess around with:

View chain state:
```
bitcoin-cli -getinfo
```

List loaded wallets:

```
bitcoin-cli listwallets
```

Create a new wallet:

```
bitcoin-cli createwallet "default"
```

Get wallet balance:

```
bitcoin-cli getbalance
```


### Get regtest coins

First you need an address:

```
bitcoin-cli getnewaddress
```

Regtest allows you to generate blocks to an address:

```
bitcoin-cli generatetoaddress 101 "address"
```

We need to mine 101 blocks so that our coinbase funds can be confirmed.

Now you can verify your balance and should see 50 BTC

```
bitcoin-cli getbalance
```

## Lightning-CLI 

If you ran the `startup_regtest.sh` script above, you should be able to use lightning-cli with the alias `l#-cli`. For example to access node 1 you would use `l1-cli`.

Use `getinfo` to see connection information:

```
l2-cli getinfo
```

In the output, you'll see the `bindings`:

```
"binding": [
      {
         "type": "ipv4",
         "address": "127.0.0.1",
         "port": 7272
      }
   ],
```

You can use the above binding along with `l2`'s pubkey to make a peer-to-peer connection. To connect to another node use `connect`:

```
l1-cli connect 038b6f8e52dc4f275d316a345e1d70566b2c1fa0f972e5eb816c0faeda69513a14@localhost:7272
```

Connect takes a connection string in the form of pubkey@host:port

Now `l1` is connected to `l2`.

To open a channel, we first need `l1` to have some bitcoin.

Get a new address for `l1`:

```
l1-cli newaddr
```

Send funds to `l1` from `bitcoind` (make sure to input the address you just generated):

```
bt-cli -named sendtoaddress address=<address> amount=1 fee_rate=25
```

Mine some blocks to get the transaction confirmed:

```
bt-cli -generate 10
```

Open a channel from `l1` to `l2`:

```
l1-cli fundchannel <l2 nodeID/pubkey> <amount>
```

`l2-cli getinfo` will get you `l2`'s ID.

Finally, get the funding transaction confirmed:

```
bt-cli -generate 10
```

Verify you've opened a channel:

```
l1-cli listchannels
```


