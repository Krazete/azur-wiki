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

python -m builddecor # build furniture page
python -m builddecor -d # update inputs first

python -m builddecorset -n <NAME> # build furniture set page
python -m builddecorset -d # update inputs first

python -m buildstory -t <TITLE> # build story pages for matching titles
python -m buildstory -d # update inputs first
python -m buildstory -p <CHARACTER> # get story titles containing sprites of matching characters
```
