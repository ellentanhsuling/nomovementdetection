#!/bin/bash

# Simple script to find Raspberry Pi on network
# Scans common IP range for devices

echo "Scanning network for Raspberry Pi..."
echo "This may take a minute..."
echo ""

# Get network range from current IP
MY_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
NETWORK=$(echo $MY_IP | cut -d. -f1-3)

echo "Your Mac IP: $MY_IP"
echo "Scanning network: $NETWORK.0 - $NETWORK.255"
echo ""

# Try common Pi IPs first (faster)
COMMON_IPS=("$NETWORK.1" "$NETWORK.2" "$NETWORK.10" "$NETWORK.20" "$NETWORK.50" "$NETWORK.100" "$NETWORK.101" "$NETWORK.102")

echo "Checking common IP addresses first..."
for ip in "${COMMON_IPS[@]}"; do
    if ping -c 1 -W 1 $ip > /dev/null 2>&1; then
        echo "✓ Found device at $ip"
        # Try to get hostname
        HOSTNAME=$(nslookup $ip 2>/dev/null | grep "name" | awk '{print $4}' | cut -d. -f1)
        if [ ! -z "$HOSTNAME" ]; then
            echo "  Hostname: $HOSTNAME"
            if [[ "$HOSTNAME" == *"raspberry"* ]] || [[ "$HOSTNAME" == *"pi"* ]]; then
                echo ""
                echo "🎉 FOUND RASPBERRY PI!"
                echo "   IP Address: $ip"
                echo "   Hostname: $HOSTNAME"
                echo ""
                echo "Try: ssh pi@$ip"
                exit 0
            fi
        fi
    fi
done

echo ""
echo "Scanning full network range (this will take longer)..."
FOUND=0
for i in {1..254}; do
    IP="$NETWORK.$i"
    if [ "$IP" != "$MY_IP" ]; then
        if ping -c 1 -W 1 $IP > /dev/null 2>&1; then
            echo "✓ Device found at $IP"
            HOSTNAME=$(nslookup $IP 2>/dev/null | grep "name" | awk '{print $4}' | cut -d. -f1)
            if [ ! -z "$HOSTNAME" ]; then
                echo "  Hostname: $HOSTNAME"
                if [[ "$HOSTNAME" == *"raspberry"* ]] || [[ "$HOSTNAME" == *"pi"* ]]; then
                    echo ""
                    echo "🎉 FOUND RASPBERRY PI!"
                    echo "   IP Address: $IP"
                    echo "   Hostname: $HOSTNAME"
                    echo ""
                    echo "Try: ssh pi@$IP"
                    FOUND=1
                    break
                fi
            fi
        fi
    fi
    # Show progress every 50 IPs
    if [ $((i % 50)) -eq 0 ]; then
        echo "  Scanned $i/254..."
    fi
done

if [ $FOUND -eq 0 ]; then
    echo ""
    echo "⚠️  Raspberry Pi not found automatically."
    echo ""
    echo "Try these options:"
    echo "1. Check router admin page: http://172.20.80.1"
    echo "2. Make sure Pi is powered on and connected to WiFi"
    echo "3. Wait 1-2 minutes after powering on Pi"
    echo "4. Use a network scanner app (Fing, LanScan, etc.)"
fi
