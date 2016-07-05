#!/bin/sh
timestamp=$(date +"%Y%m%d%H%M%S")
filename="export-$timestamp"".csv"
sudo mongoexport -h localhost:81 --db meteor --collection answers --fieldFile exportfields.txt --type csv -o "$filename"