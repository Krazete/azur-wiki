# Azur Lane Wiki Tools

Tools I made to help me edit pages on the [Azur Lane Wiki](https://azurlane.koumakan.jp).

## Setup
```sh
python -m venv venv
venv\Scripts\activate # windows
source venv\bin\activate # mac
pip install -r requirements.txt
```

## Scripts
```sh
python -m preabextract # update output/skinname.json for abextract to use in azur-paint command list
python -m abextract # extract files from AssetBundles and build command list for azur-paint
# execute abget.sh first to extract latest AssetBundles files from phone (adb required)

python -m <SCRIPT> -d # (re)download prerequisite input data for <SCRIPT>

python -m buildchild # build tb page

python -m builddecor # build furniture table

python -m builddecorset # build table of furniture items not part of a set
python -m builddecorset -s <SET NAME> # build furniture set table
python -m builddecorset -l <LANGUAGE> -s <SET NAME> # build furniture set table in CN or JP
python -m builddecorset -i <ITEM NAME> # build furniture item entries
python -m builddecorset -e # include last `|` in lines with no note

python -m buildgearskin # build table of all gear skins
python -m buildgearskin -s <SET NAME> # build gear skin box table

python -m buildjuustagram # (not yet implemented)

python -m buildskinname # build list of ship skin names

python -m buildstory -t <TITLE> # build story tables for matching title
python -m buildstory -t <TITLE> -i 1 # build story tables for matching title and result index
python -m buildstory -p <CHARACTER> # get story titles containing sprites of matching characters
python -m buildstory -p <BGNAME> # get story titles containing specified backgrounds

python -m buildstoryvoice # build list of voice audio files used within stories

python -m buildcollect # build Collection Archives page

python -m buildmedal -e # extract and rename medal images from AssetBundles
python -m buildmedal -b # build Medallion page

python -m buildui # build page for Battle UI

python -m buildhall # build Hall of Fame section for Memories page

python -m buildtask # build event missions tables

python -m builddrawingbook # export drawingbooks (images and Template:DrawingBook wikitext)

python -m buildsirenquote # build quote pages for special secretaries
```
