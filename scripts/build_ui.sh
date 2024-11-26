#!/bin/bash

# Determine the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if npm is installed
if ! command -v node &> /dev/null
then
    echo "Node.JS is not installed. Please install Node.JS to continue."
    exit 1
fi

# Run npm install and npm build in the ui/ directory
npm --prefix "$SCRIPT_DIR/../ui" install
npm --prefix "$SCRIPT_DIR/../ui" run build