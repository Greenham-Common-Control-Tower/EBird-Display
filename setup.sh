#!/bin/bash

# Configuration
REPO_URL="https://forge.lawridarbyshire.co.uk/Darbyshire64/LawriBirdProgram.git"
APP_DIR="$HOME/LawriBirdProgram"
SERVICE_NAME="lawribirdboard"
PYTHON_BIN="$APP_DIR/venv/bin/python3"
USERNAME="Tower"


echo ">>> Setting up virtual Python environment..."
python3 -m venv venv
source venv/bin/activate

echo ">>> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> Writing systemd service file..."

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=LawriBird Observation Web App
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN main.py && update.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo ">>> Reloading systemd and starting service..."
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo ">>> Checking service status..."
sleep 1
sudo systemctl status $SERVICE_NAME --no-pager

echo ">>> Done. The app should now be running at http://localhost:1991/"
echo ">>> Please Update The API Key in main py to your own"