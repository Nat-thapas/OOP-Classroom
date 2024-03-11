#!/bin/sh
cd /
uvicorn "app.main:app" --host "0.0.0.0" --port 8080 &
node /frontend/build
