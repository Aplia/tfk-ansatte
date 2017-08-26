#!/usr/bin/env bash
WATCHER=${WATCHER-ember serve --live-reload-port=$WEB_PORT}

echo "Installing npm packages"
yarn install

echo "Starting gulp watch and livereload"
echo "nodemon --exec \"${WATCHER}\""
echo "$PATH"
nodemon --exec "${WATCHER}"
