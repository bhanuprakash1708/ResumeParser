#!/bin/bash
# Location: /setup.sh

echo "--- [AI Resume Parser] Starting Project Setup ---"

# 1. Check for Python 3.10+
echo "Checking Python version..."
if ! python3 --version &> /dev/null; then
    echo "ERROR: python3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# 2. Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment 'venv'..."
    python3 -m venv venv
else
    echo "Virtual environment 'venv' already exists."
fi

# 3. Activate the virtual environment
source venv/bin/activate
echo "Virtual environment activated."

# 4. Install Python dependencies
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# 5. Create the .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "IMPORTANT: Please edit the .env file with your GEMINI_API_KEY."
else
    echo ".env file already exists."
fi

# 6. Inform user to start Docker
echo ""
echo "--- Setup Complete! ---"
echo "To run the application, make sure Docker Desktop is running and then execute:"
echo ""
echo "docker compose -f docker/docker-compose.yml down -v"
echo "docker compose -f docker/docker-compose.yml build --no-cache"
echo "docker compose -f docker/docker-compose.yml up"
echo ""
echo "You can then access the API docs at http://localhost:8000/docs"