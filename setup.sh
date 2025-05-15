#!/bin/bash

# Config
APP_DIR="/home/tower/LawriBirdProgram"
SERVICE_NAME="lawribird"
PYTHON_BIN="$APP_DIR/venv/bin/python3"

echo ">>> Moving to app directory..."
cd "$APP_DIR" || { echo "App directory not found!"; exit 1; }

echo ">>> Creating virtual environment..."
python3 -m venv venv

echo ">>> Installing dependencies inside venv..."
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt

echo ">>> Creating systemd service file..."

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=LawriBird Observation Web App
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo ">>> Reloading and enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo ">>> Checking service status..."
sleep 1
sudo systemctl status "$SERVICE_NAME" --no-pager

echo ">>> Setup complete. App should be running at http://localhost:1991/"
