#!/bin/bash


check_python_version() {
    PYTHON_VERSION=$(python3 --version 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "Python 3 is not installed. Please install Python 3.9+."
        exit 1
    fi

    REQUIRED_VERSION="3.9"
    CURRENT_VERSION=$(echo $PYTHON_VERSION | grep -o '[0-9]\.[0-9]')
    if (( $(echo "$CURRENT_VERSION < $REQUIRED_VERSION" | bc -l) )); then
        echo "Python version must be 3.9 or higher. Current version: $CURRENT_VERSION"
        exit 1
    fi
}

# install Python dependencies
install_dependencies() {
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    if [[ $? -ne 0 ]]; then
        echo "Failed to install dependencies. Please ensure pip is installed and configured."
        exit 1
    fi
}

# Function to validate .env file
validate_env_file() {
    if [[ ! -f ".env" ]]; then
        echo ".env file is missing."
        read -p "Would you like to create a .env file interactively? (y/n): " create_env
        if [[ $create_env == "y" || $create_env == "Y" ]]; then
            create_env_file
        else
            echo "Please create a .env file based on .env.example before proceeding."
            exit 1
        fi
    fi
}

#  create .env file interactively
create_env_file() {
    read -p "Enter AWS Access Key ID: " AWS_ACCESS_KEY_ID
    read -p "Enter AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
    read -p "Enter AWS Default Region [us-east-1]: " AWS_DEFAULT_REGION

    AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-us-east-1}

    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" > .env
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env
    echo "AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION" >> .env

    echo ".env file created successfully!"
}

# register the CLI globally
register_cli() {
    read -p "Would you like to register this CLI globally? (y/n): " register
    if [[ $register == "y" || $register == "Y" ]]; then
        SCRIPT_PATH=$(pwd)/aws_cli_tool.py
        echo "alias awscli='python3 $SCRIPT_PATH'" >> ~/.bashrc
        source ~/.bashrc
        echo "CLI registered as 'awscli'. You can now run commands like 'awscli sqs list'."
    fi
}


echo "Starting setup process..."
check_python_version
install_dependencies
validate_env_file
register_cli
echo "Setup completed successfully!"
