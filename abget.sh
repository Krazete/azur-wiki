#!/bin/bash
# todo: ask to delete current AssetBundles folder
# todo: ask what number of days is considered new
# retrieve all files with a last modified time of a week ago or less
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
        age=$(($now - $mtime - 7*86400)) # date difference minus a week
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
