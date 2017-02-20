#!/bin/bash

cd data/
ls -U | head -100 > ../nombres.txt
cd ..
while read p; do
	IFS='.' read -r -a array <<< "$p"
	pdftotext data/$p data/"${array[0]}.txt"
done < nombres.txt