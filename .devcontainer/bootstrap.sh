#!/usr/bin/env bash

cd /academia.fyi

source /opt/conda/etc/profile.d/conda.sh
conda env create -f .devcontainer/environment.yml
conda activate academia-fyi

sudo apt install -y libpq-dev
