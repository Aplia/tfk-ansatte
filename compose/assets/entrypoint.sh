#!/usr/bin/env bash
set -e
cmd="$@"

export PATH="/app/node_modules/.bin:$HOME/.yarn/bin/:$PATH"

exec $cmd
