# Setting Up A CLN Dev Environment

> **Livestreaming Sunday October, 22 @ 1pm PT -- 3pm CT -- 4pm ET**

- [Introduction](#introduction)
- [Instructions](#instructions)
- [Installing Bitcoin Core](#installing-bitcoin-core)
- [Installing CLN](#installing-cln)
- [Configuring Bitcoin Core](#bitcoin-config)

**v v v still a WIP v v v**
- [Learn bitcoin-cli](#bitcoin-cli)
- [Learn lightning-cli](#lightning-cli)

**^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^**

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

**EVERYTHING BELOW IS STILL A WIP**

CLN start up regtest
startup_regtest.sh

## Bitcoin-CLI

`bitcoin-cli -getinfo`

```

bitcoin-cli listwallets

```

```

alias bt-cli="bitcoin-cli"

```

```

bitcoin-cli createwallet "plugindev"

```

```

bitcoin-cli listwallets

```

## Lightning-CLI


