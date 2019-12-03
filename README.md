# Code Challenge
## Overview

This repository contains code for the code challenge described in README2.md.

## ETL Engineering Challenge Setup
MySQL provides a python connector for database management.
In order to run, make sure python3.7 is installed, install mysql-connector-python with pip as described here: https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html.

If not already installed, pip install argparse & csv.

The script requires a password and the directory where the mapping/data csv files are located.
Simply run `python3 loadData.py ./datamap [password]` where password is the password for root user of MySQL connection.
*Password is an optional argument in the case that no password is required for root

## Web Service/JS Engineering & UI/UX Challenge Setup
Ensure node is installed on your machine, then run `npm i` within the code-challenge directory.
After all required packages are installed, run `node server.js [password]` where password is the password for root user of MySQL connection. If no password, run `node server.js`.
