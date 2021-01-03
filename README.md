# SRT Translator
This is a simple python script for translating SRT(SubRip) files to other languages using Google translation API.

# Requirements
* python >= 3.0 (https://www.python.org/downloads/)
* python modules
  - lxml
  - cssselect
```
  python -m pip install requests
  python -m pip install lxml
  python -m pip install cssselect
```

# Usage

```
usage: smart_shampoo.py [-h] [-sl ko] [-l en zh-TW [en zh-TW ...]] source.srt

positional arguments:
  source.srt            srt file path that you want to translate.

optional arguments:
  -h, --help            show this help message and exit
  -sl ko, --sl ko       language code of input srt file
  -l en zh-TW [en zh-TW ...], --language en zh-TW [en zh-TW ...]
                        language codes those you want to translate.
```
```
# ex. Translating Korean subtitles into English and Taiwanese subtitles
> python smart_shampoo.py source.srt -sl ko -l en zh-TW
```
