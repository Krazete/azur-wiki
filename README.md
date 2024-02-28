# Azur Lane Wiki Tools

Tools I've made to help me edit pages on the [Azur Lane Wiki](https://azurlane.koumakan.jp).

|Script|Wiki Page|
|--|--|
|itemchart.py|[Project Identity: TB](https://azurlane.koumakan.jp/wiki/Project_Identity:_TB)|
|decorchart.py|[Decorations](https://azurlane.koumakan.jp/wiki/Decorations#List_of_Furniture_Sets)|

## Instructions

```sh
python -m venv venv

venv\Scripts\activate # windows
source venv\bin\activate # mac

pip install -r requirements.txt

python -m itemchart
python -m decorchart -d # update input/decorchartnow.txt first
```
