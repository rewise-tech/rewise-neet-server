#! /usr/bin/env bash

set -e
set -x

# Create initial data in DB
python -m app.db.init_db
