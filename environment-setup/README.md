# Building A CLN Dev Environment

Getting everything properly installed and running on a development machine is frustrating for me, so I hope these docs are clear and helpful to getting you on your way to building CLN plugins.

C-Lightning has a plugin architecture that allows plebs to write custom code, and run it on their node using any programming language.

To do this, we will first need to set up a test environment consisting of 1 `bitcoind` instance and multiple `lightningd` instances. You can think of these as applications.

In this workshop we will be building CLN from source and installing Bitcoin Core using `snapd`.

Final notes before getting into it:

> _These instructions are based on Ubuntu 22.04. Ask for help if you have trouble_
>
> This is a trimmed-down version of the CLN [install docs](https://github.com/ElementsProject/lightning/blob/master/doc/getting-started/getting-started/installation.md)

**Instructions**:

Copy the commands into your bash terminal. If you're on *Ubuntu 22.04* this should build smooth, but different OSes will have different results. Usually copy & pasting your error into Chat-GPT/Google will help you find the missing packages.

The end **goal** is to have some nodes built and running on your local machine for convenient plugin development.

## Installing Bitcoin Core

We will just use snapd because its much simpler, but if you haven't yet it's worth it to try building Bitcoin Core from source.

```
sudo apt-get install snapd #install the snap package manager
sudo snap install bitcoin-core # use snap to install the `bitcoin-core` package
# Snap does some weird things with binary names; you'll
# want to add a link to them so everything works as expected
sudo ln -s /snap/bitcoin-core/current/bin/bitcoin{d,-cli} /usr/local/bin/
```

*I'll try to leave helpful comments in the install commands, so don't just blindly copy and paste.*

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

### clone

```
git clone https://github.com/ElementsProject/lightning.git
cd lightning
```

### Checkout release branch

```
git checkout v22.11.1
```

### activate venv

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

Run the [Makefile](https://github.com/ElementsProject/lightning/blob/master/Makefile) script and install

```
make
sudo make install
```

## Bitcoin Config

Now you should have `bitcoind` and `lightningd` in your PATH

Run `bitcoind -regtest` to start and create `~/.bitcoin`;

```

cd .bitcoin
touch bitcoin.conf

```

set bitcoin.conf to regtest=1

##

CLN start up test
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

```

bitcoin-cli

```

```

```
