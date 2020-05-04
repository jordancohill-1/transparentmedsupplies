#!/bin/bash

pip install --upgrade pip

# Previous class: install Anaconda/Miniconda
# wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
# bash Anaconda3-2018.12-Linux-x86_64.sh



# conda create -n <env_name> python=3.6   #  -> # create new environment with python 3.6, for example 
# conda activate <env_name>               #  -> # go into the virtual environment
# chmod u+x ethereum_install.sh           #:might be necessary
# bash ethereum_install.sh <env_name>



myenv=$1 # this means first command line variable/ not file name



apt-get install git # install git to install py-ethereum



pip install jupyter # could attach version number
head_name="Python ("
middle_name=$myenv
tail_name=")"
full_name="$head_name$myenv$tail_name"  # string concatenation



# create block_env environment within notebooks
python3 -m pip install ipykernel
python3 -m pip install ipykernel --user
python3 -m ipykernel install --user --name $myenv --display-name "$full_name"



# old ecdsa install
pip install ecdsa



# py-ethereum and tester
sudo apt-get install libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libyaml-cpp-dev
git clone https://github.com/ethereum/pyethereum/
cd pyethereum
python setup.py install
pip install web3
pip install -U "web3[tester]"


sudo apt update



# install Solidity compiler
pip install py-solc-x
python -m solcx.install v0.4.25


