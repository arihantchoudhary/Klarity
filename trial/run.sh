#!/bin/bash

# Function to cleanup background processes on exit
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Create necessary directories if they don't exist
mkdir -p uploads vector_store content static

# Check if conda environment exists and activate it
if conda env list | grep -q "klarity"; then
    echo "Activating conda environment 'klarity'..."
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate klarity
else
    echo "Conda environment 'klarity' not found. Please create it first."
    exit 1
fi

# Start the backend server
echo "Starting backend server..."
cd backend
python app.py &

# Wait a moment for the backend to start
sleep 2

# Start the frontend server
echo "Starting frontend server..."
cd ..
python -m http.server 8000 &

echo "Servers are running!"
echo "Frontend: http://localhost:8000"
echo "Backend: http://localhost:5001"
echo "Press Ctrl+C to stop both servers"

# Wait for all background processes
wait 