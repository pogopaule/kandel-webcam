#!/bin/bash

date=$(date +"%d-%m-%y")
mkdir $date

for hour in {8..21}
do
  paddedHour=$(printf "%02d" $hour)
  for minute in 00 15 30 45
  do
    wget http://www.dgfc-suedschwarzwald.de/webcam2/image-${paddedHour}-${minute}.jpg -O $date/$paddedHour-${minute}.jpg
  done
done


