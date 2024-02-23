#!/bin/bash

#  copy the db
cd ~/.mozilla/firefox/n30kh9ge.default-release-old
# cd ~/.mozilla/firefox/h88v97w8.h
cp places.sqlite ~/project/historyblob/csv
# create csvs
cd ~/project/historyblob/csv
bash ../convert-db-to-csv/convert-db-to-csv.sh places.sqlite
# run script
cd ..
source .venv/bin/activate
python hist2cloud.py
# copy img to github repo
cp wordcloud.png ../roblee04.github.io/
cd ../roblee04.github.io/
git pull
# push changes
git add *
git commit -m "update wordcloud"
git push -u origin main
