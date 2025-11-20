#!/bin/bash

# WebCrawlerAPI Standalone SDK - Compile and Run Script
# This script compiles and runs the example application

set -e  # Exit on error

echo "WebCrawlerAPI Standalone SDK - Example"
echo "======================================="
echo

# Check Java version
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed"
    echo "Please install Java 17 or newer"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | awk -F '.' '{print $1}')
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "Error: Java 17 or newer is required"
    echo "Current version: $(java -version 2>&1 | head -n 1)"
    exit 1
fi

echo "Java version: $(java -version 2>&1 | head -n 1)"
echo

# Check for API key
if [ -z "$API_KEY" ]; then
    echo "Error: API_KEY environment variable is not set"
    echo
    echo "Usage:"
    echo "  API_KEY=your-api-key ./compile-and-run.sh"
    echo
    echo "For local testing:"
    echo "  API_KEY=test-api-key API_BASE_URL=http://localhost:8080 ./compile-and-run.sh"
    exit 1
fi

# Create bin directory
mkdir -p bin

# Copy SDK file to current directory
echo "Copying WebCrawlerAPI.java..."
cp ../../java/standalone-sdk/WebCrawlerAPI.java .

# Compile
echo "Compiling Java files..."
javac *.java -d bin

if [ $? -eq 0 ]; then
    echo "Compilation successful!"
    echo
    echo "Running example..."
    echo "==================="
    echo

    # Run the example
    java -cp bin Example
else
    echo "Compilation failed!"
    exit 1
fi
