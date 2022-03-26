#!/bin/bash

interface=$1

echo "taking down ${interface}"
sudo ifconfig ${interface} down

#echo "cleaning (airmon-ng check kill)"
#airmon-ng check kill

echo "changing to monitor mode"
sudo iwconfig ${interface} mode managed

echo "bringing ${interface} up"
sudo ifconfig ${interface} up

echo "done"
