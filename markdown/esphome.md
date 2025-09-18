sudo apt update
# Install Python & pip if missing
sudo apt install python3 python3-pip python3-venv -y

# Install ESPHome
pip install --user esphome

# Check if installed correctly
esphome version

