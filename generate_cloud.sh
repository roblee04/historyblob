#!/bin/bash

#  copy the db
cd ~/home/robin/.mozilla/firefox/n30kh9ge.default-release-old
cp places.sqlite ~/project/historyblob/
# create csvs
cd ~/project/historyblob/csv
bash ../convert-db-to-csv/convert-db-to-csv.sh
# run script
cd ..
python hist2cloud.py
# copy img to github repo
cp wordcloud.png ../roblee04.github.io/
# push changes
git add *
git commit -m "update wordcloud"
git push -u origin main
