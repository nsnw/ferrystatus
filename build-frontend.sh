#!/bin/bash

# Set directories
APP_DIR="/app"
NODE_DIR="/opt/nodejs"

# Set node download details
NODEJS_VERSION="v10.15.3"
NODEJS_URL="https://nodejs.org/dist/${NODEJS_VERSION}/node-${NODEJS_VERSION}-linux-x64.tar.xz"

# Create install dir
mkdir -pv ${NODE_DIR}

# Download NodeJS
wget -O /tmp/nodejs.tar.xz ${NODEJS_URL}

# Unpack NodeJS to install dir
tar -xvf /tmp/nodejs.tar.xz -C ${NODE_DIR} --strip-components=1

# Add node to the PATH
export PATH="${PATH}:/opt/nodejs/bin"

# Install Webpack
npm install webpack webpack-cli

# Build frontend
cd ${APP_DIR}
npm run all:prod