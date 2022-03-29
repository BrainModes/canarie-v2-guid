#!/bin/bash
waitress-serve --port=5000 --call 'application:create_app'
