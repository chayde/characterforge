#!/bin/bash
export PYTHONPATH=$PYTHONPATH:.
./venv/bin/uvicorn backend.app.main:app --reload --port 8000
