#!/bin/bash
clear
python cfg_bb.py $1
python dom_sets.py
read -p "Press any key to continue" x