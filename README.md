# Automated-Google-Maps-Screenshot-Taker
Tool for generating large number of screenshots using selenium

This tool can be used for generating a large quantity of screenshots (in this case Google Maps) from an xlsx file using a browser automation tool called Selenium. You can search for the file using autocompletion in the terminal and also use this feature to chose the destination folder for saving the timestamped folder containing the images. The generated screenshots are stored in the same directory as the python script in case of any errors. Ensure that all the dependencies have been installed on the system before running.Use the following commands on a Windows machine preferably running python 3.6 or later.

```sh
python -m pip install selenium -users
python -m pip install xlrd -users
python -m pip install Pillow -users
python -m pip install colorama -users
python -m pip install pyreadline -users
```
Do not forget do installl the chromedriver for your latest version of Google Chrome and set in the path variables.
