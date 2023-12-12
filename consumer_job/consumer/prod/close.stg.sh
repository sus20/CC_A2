#!/bin/bash

# Function to kill port-forwarding processes
kill_port_forward() {
    local port=$1

    # Identify PIDs of processes that are port-forwarding the specified port
    local pids=$(lsof -ti tcp:$port)

    # Kill the processes if they exist
    if [ -n "$pids" ]; then
        echo "Stopping port-forwarding on port $port..."
        kill -9 $pids
    fi
}

# Stop kafdrop
kill_port_forward 9000

# stop consumer-app
kill_port_forward 8000