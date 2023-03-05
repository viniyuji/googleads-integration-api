#!/bin/sh

nginx -g 'daemon off;' &
gunicorn --bind 0.0.0.0:8000 configs.wsgi