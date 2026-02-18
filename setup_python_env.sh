#!/bin/bash

echo "Updating system..."
sudo apt update

echo "Installing Python, venv, pip, and Firefox..."
sudo apt install -y python3 python3-venv python3-pip firefox python3-tk scrot  xclip

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements if file exists
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. Installing dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

echo "Setup complete!"

# Pause before exit
read -p "Press Enter to exit..."
