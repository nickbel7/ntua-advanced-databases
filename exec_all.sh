#!/bin/bash

for i in {1..5}; do
  python3.8 query_$i.py
done

python3.8 plot.py