#!/bin/bash

if [ -d AssetBundles ]; then
    read -p "AssetBundles directory exists. Delete it? (y/n)"$'\n' delab
    if [[ $delab == [Yy] ]]; then
        rm -r AssetBundles
        echo "AssetBundles deleted."
    else
        echo "AssetBundles retained."
    fi
fi

adb start-server

read -p "Enter the age (in days; add \"h\" for hours) of files to extract."$'\n' timespan
if [[ ! $timespan =~ ^[0-9]+h?$ ]]; then
    echo "Error: Invalid timespan. Exiting..."
    sleep 2
    exit 1
fi
if [[ $timespan == *h ]]; then
    secs=$((${timespan:0:-1} * 3600))
else
    secs=$(($timespan * 86400))
fi

# retrieve all files with a last modified time of $secs seconds ago or later
now=$(date +%s)
filelist=$(adb shell ls -Rpgot sdcard/Android/data/com.YoStarEN.AzurLane/files/AssetBundles) # sort by and include last modified time (mtime)
while IFS=$'\t\r\n' read -r line; do
    if [[ $line == *: ]]; then
        parent=${line:0:-1} # remember parent folder
    elif [[ $line == */ ]]; then
        continue # ignore subfolders
    elif [[ $parent != "" && $line =~ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})" "(.+) ]]; then
        stamp=${BASH_REMATCH[1]} # date and time; format: "1970-01-01 00:00"
        mtime=$(date -d "$stamp" +%s) # stamp in seconds
        # mtime=$(adb shell -n stat -c %Y $srcpath) # unused alternative; too expensive and slow
        age=$(($now - $mtime - $secs)) # date difference minus $secs seconds
        if [[ $age == -* ]]; then
            name=${BASH_REMATCH[2]}
            srcpath=$parent/$name # file path on phone
            dstparent=${parent:48}
            mkdir -p $dstparent # create folder on computer
            dstpath=$dstparent/$name # file path for computer
            adb pull -a $srcpath $dstpath # copy file with mtime preserved
        else
            parent="" # after encountering one old file, ignore the rest of the file list for the parent folder
        fi
    fi
done <<< "$filelist"

echo "Extraction complete."
read -p "Press any key to exit." -r -n 1 -s
