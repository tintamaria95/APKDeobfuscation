#! /bin/sh
for file in ./scraped_data/*.zip
    do
        unzip $file -d ./apps/
    done