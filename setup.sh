#!/bin/bash
set -e  # Exit on any error

# ============================================================================
# Configuration
# ============================================================================
APP_DIR="/home/tower/LawriBirdProgram"
SERVICE_NAME="lawribird"
PYTHON_BIN="$APP_DIR/venv/bin/python3"
PORT="1991"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================
print_step() {
    echo -e "${GREEN}>>> $1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_info() {
    echo -e "${BLUE}$1${NC}"
}

ask_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# ============================================================================
# Main Installation
# ============================================================================
print_step "Starting LawriBird installation..."

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. Consider running as a regular user with sudo access."
fi

# Navigate to app directory
print_step "Navigating to app directory: $APP_DIR"
if [ ! -d "$APP_DIR" ]; then
    print_error "App directory not found: $APP_DIR"
    exit 1
fi
cd "$APP_DIR"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in $APP_DIR"
    exit 1
fi

# Create virtual environment
print_step "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Recreating..."
    rm -rf venv
fi
python3 -m venv venv

# Upgrade pip and install dependencies
print_step "Installing dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip --quiet
"$PYTHON_BIN" -m pip install -r requirements.txt --quiet

# Ask user about service installation
echo ""
print_info "=========================================="
print_info "Service Installation Options"
print_info "=========================================="
echo ""
echo "Do you want to install a systemd service?"
echo "  YES: App will auto-start on boot"
echo "  NO:  You'll need to manually run: $PYTHON_BIN main.py"
echo ""

if ask_yes_no "Install systemd service?"; then
    INSTALL_SERVICE=true
else
    INSTALL_SERVICE=false
fi

if [ "$INSTALL_SERVICE" = true ]; then
    # Create systemd service
    print_step "Creating systemd service..."
    SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=LawriBird Observation Web App
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # Enable and start service
    print_step "Enabling and starting service..."
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl restart "$SERVICE_NAME"

    # Wait for service to start
    print_step "Waiting for service to start..."
    sleep 2

    # Check service status
    print_step "Checking service status..."
    if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
        echo -e "${GREEN}✓ Service is running successfully!${NC}"
        sudo systemctl status "$SERVICE_NAME" --no-pager -l
    else
        print_error "Service failed to start. Check logs with: sudo journalctl -u $SERVICE_NAME -n 50"
        exit 1
    fi

    # Final message for service installation
    echo ""
    echo -e "${GREEN}============================================================================${NC}"
    echo -e "${GREEN}Installation complete with systemd service!${NC}"
    echo -e "${GREEN}============================================================================${NC}"
    echo ""
    echo "App is running at: http://localhost:$PORT/"
    echo ""
    echo "Useful commands:"
    echo "  View logs:     sudo journalctl -u $SERVICE_NAME -f"
    echo "  Stop service:  sudo systemctl stop $SERVICE_NAME"
    echo "  Start service: sudo systemctl start $SERVICE_NAME"
    echo "  Restart:       sudo systemctl restart $SERVICE_NAME"
    echo "  Disable:       sudo systemctl disable $SERVICE_NAME"
    echo ""
else
    # Manual start instructions
    echo ""
    echo -e "${GREEN}============================================================================${NC}"
    echo -e "${GREEN}Installation complete (manual mode)!${NC}"
    echo -e "${GREEN}============================================================================${NC}"
    echo ""
    echo "To start the application manually, run:"
    echo -e "  ${YELLOW}cd $APP_DIR${NC}"
    echo -e "  ${YELLOW}$PYTHON_BIN main.py${NC}"
    echo ""
    echo "The app will be available at: http://localhost:$PORT/"
    echo ""
    echo "To install the service later, run this script again or use:"
    echo "  sudo systemctl enable $SERVICE_NAME"
    echo "  sudo systemctl start $SERVICE_NAME"
    echo ""
fi