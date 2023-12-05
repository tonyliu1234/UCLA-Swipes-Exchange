#!/bin/bash

# Move to the backend directory
cd backend

# Copy the contents to the root directory of the Heroku app
cp -R ./* ..

# Move back to the root
cd ..
