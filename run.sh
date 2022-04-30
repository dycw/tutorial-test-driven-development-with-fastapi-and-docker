#!/usr/bin/env bash

cd src || exit
uvicorn app.main:app
