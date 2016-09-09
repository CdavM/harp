#!/bin/sh
pem_file="turkexperiments.pem"
timestamp=$(date +"%Y%m%d%H%M%S")
filename="export-$timestamp"".csv"
ssh -i "$pem_file" ubuntu@52.53.186.8 filename=$filename 'bash -s' <<'ENDSSH'
cd harp/private
sudo mongoexport -h localhost:81 --db meteor --collection answers --fieldFile exportfields.txt --type csv -o "$filename"
ENDSSH
scp -i "$pem_file" ubuntu@52.53.186.8:/home/ubuntu/harp/private/$filename . 
