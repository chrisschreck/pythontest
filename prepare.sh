#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt update
apt upgrade -y
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install python3.11 -y
apt install python3.11-full -y
apt install python3.11-venv -y
pip install -U pip
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt