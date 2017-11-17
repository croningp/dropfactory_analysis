#!/bin/bash

# I use this kind of script because of memory issues, after a few dozen experiments the RAM is not cleaned up

# this way python is shutdown after each batch, hence freeing the memory

while true; do
   python analyse_videos.py
done
