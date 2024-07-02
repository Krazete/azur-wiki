#!/bin/bash
# retrieve all files with a last modified time of a week ago or less
now=$(date +%s)
filelist=$(adb shell ls -Rpgot sdcard/Android/data/com.YoStarEN.AzurLane/files/AssetBundles)
while IFS=$'\t\r\n' read -r line; do
    if [[ $line == *: ]]; then
        parent=${line:0:-1} # parent folder
    elif [[ $line == */ ]]; then
        continue # ignore subfolders
    elif [[ $parent != "" && $line =~ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})" "(.+) ]]; then
        # age=$(adb shell -n stat -c %Y $filename) # get last modified time in seconds of individual file
        stamp=${BASH_REMATCH[1]} # date and time (1970-01-01 00:00)
        mtime=$(date -d "$stamp" +%s) # stamp in seconds
        age=$(($now - $mtime - 7*86400)) # 1 day = 86400
        if [[ $age == -* ]]; then
            name=${BASH_REMATCH[2]} # file name
            path=$parent/$name # file path
            mkdir -p $parent
            adb pull $path $path
        else
            parent="" # after one old file, ignore the rest of the list
        fi
    fi
done <<< "$filelist"
