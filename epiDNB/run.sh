#!/bin/bash

python generate_obs.py

./train_cmd.sh data/dbn_train_100.txt 
./test_cmd.sh data/dbn_train_100.txt 