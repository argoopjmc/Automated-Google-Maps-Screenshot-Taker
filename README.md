# Automated-Google-Maps-Screenshot-Taker
Tool for generating large number of screenshots using selenium

This tool can be used for generating a large quantity of screenshots (in this case Google Maps) from an xlsx file using a browser automation tool called Selenium. You can search for the file using autocompletion in the terminal and also use this feature to chose the destination folder for saving the timestamped folder containing the images. Please ensure that the file name/folder does not contain any spaces and the xlsx file contains all the heading in the first row otherwise you might face an issue while running the program.

The generated screenshots are stored in the same directory as the python script in case of any errors. Ensure that all the dependencies have been installed on the system before running.Use the following commands on a Windows machine preferably running python 3.6 or later.

```sh
python -m pip install selenium --user
python -m pip install xlrd --user
python -m pip install Pillow --user
python -m pip install colorama --user
python -m pip install pyreadline --user
```
Do not forget do installl the chromedriver for your latest version of Google Chrome and set in the path variables.
[![HitCount](http://hits.dwyl.io/argoopjmc/Automated-Google-Maps-Screenshot-Taker.svg)](http://hits.dwyl.io/argoopjmc/Automated-Google-Maps-Screenshot-Taker)
