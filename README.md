# Azur Lane Wiki Tools

Tools I've made to help me edit pages on the [Azur Lane Wiki](https://azurlane.koumakan.jp).

|Script|Wiki Page|
|--|--|
|builditem.py|[Project Identity: TB](https://azurlane.koumakan.jp/wiki/Project_Identity:_TB)|
|builddecor.py|[Decorations](https://azurlane.koumakan.jp/wiki/Decorations#List_of_Furniture_Sets)|

## Instructions

```sh
python -m venv venv
venv\Scripts\activate # windows
source venv\bin\activate # mac
pip install -r requirements.txt

python -m builditem # build tb page

python -m builddecor # build furniture table
python -m builddecor -d # (re)download prerequisite input data

python -m builddecorset # build table of furniture items not part of a set
python -m builddecorset -s <SET NAME> # build furniture set table
python -m builddecorset -i <ITEM NAME> # build furniture item entries
python -m builddecorset -e # include last `|` in lines with no note
python -m builddecorset -d # (re)download prerequisite input data

python -m buildequipskin # build table of all gear skins
python -m buildequipskin -s <SET NAME> # build gear skin box table
python -m buildequipskin -d # (re)download prerequisite input data

python -m buildstory -t <TITLE> # build story tables for matching titles
python -m buildstory -p <CHARACTER> # get story titles containing sprites of matching characters
python -m buildstory -d # (re)download prerequisite input data

python -m buildskinname # build list of ship skin names
python -m buildskinname -d # (re)download prerequisite input data

python -m abextract # extract files from AssetBundles and build command list for azur-paint
# execute abget.sh to get the latest AssetBundles files first
```
