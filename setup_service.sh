#!/bin/sh

# Get current path and user
curr_path=$(pwd)
curr_user="${SUDO_USER:-$(whoami)}"

# Replace user and path in service file, and redirect output to systemd/ directory
sed -e "s|{PATH}|$curr_path|g" -e "s|{USER}|$curr_user|g" \
    quicksaver.service > /etc/systemd/system/quicksaver.service

# Reload 'systemd' and enable the service
sudo systemctl daemon-reload
sudo systemctl enable quicksaver.service
