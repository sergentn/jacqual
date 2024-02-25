# jacqual - jacquard knit generator

This simple script generates a jacquard knit schema from an input image.

## Install
Tested with Python 3.10.12 on Ubuntu 22.04 as of 2024, February the 25th.

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage
Give it a try using the provided example image (credits: Wim Hoek)

```
python3 jacqual.py example_input_image.jpeg 130 100 4 15 1
```

Enjoy
Nicolas Sergent
