#!/bin/bash

filelist=$(ls AssetBundles/island/character)
while IFS=$'\t\r\n' read -r line; do
    filelist2=$(ls "AssetBundles/island/character/$line")
    while IFS=$'\t\r\n' read -r line2; do
        rm "C://Users/Tim/Desktop/New folder/island/character/$line${line2:0:-1}"
        mv "AssetBundles/island/character/$line$line2" "C://Users/Tim/Desktop/New folder/island/character/$line"
    done <<< "$filelist2"
done <<< "$filelist"

echo "Extraction complete."
read -p "Press any key to exit." -r -n 1 -s
