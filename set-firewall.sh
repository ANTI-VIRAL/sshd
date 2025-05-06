#!/bin/bash

# IP dan PORT VPS RELAY kamu
RELAY_IP="135.148.227.129"
RELAY_PORT="11002"

# FLUSH tapi jaga koneksi SSH biar gak lost
sudo iptables -F
sudo iptables -X

# Default policy
sudo iptables -P OUTPUT DROP
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD DROP

# Allow koneksi SSH (jaga jangan keputus ya sayang)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Allow relay pool proxy
sudo iptables -A OUTPUT -p tcp -d $RELAY_IP --dport $RELAY_PORT -j ACCEPT

# Allow DNS (kalau pakai domain)
sudo iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

# Allow localhost
sudo iptables -A OUTPUT -o lo -j ACCEPT

# (Optional) Simpan rules
sudo apt-get install iptables-persistent -y
sudo netfilter-persistent save
