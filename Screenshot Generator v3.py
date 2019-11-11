import sys
from selenium import webdriver
import os
import time
import re
import readline
import xlrd
from datetime import datetime 
from PIL import Image

string_truncate = 0

def convertTuple(tup): 
    string = ''.join(str(tup)) 
    return string

def fullpage_screenshot(driver, file):

        print("Starting chrome full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                time.sleep(2)
                driver.execute_script("document.getElementById('topnav').setAttribute('style', 'position: absolute; top: 0px;');")
                time.sleep(2)
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(2)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return True


  
COMMANDS = ['input','use', 'genfrom' , 'takeshots'  ,'savein']
RE_SPACE = re.compile('.*\s+$', re.M)
test_var= ""
class Completer(object):

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_input(self, args):
        "Completions for the 'input' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])
        
    def complete_use(self, args):
        "Completions for the 'genfrom' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])

    def complete_takeshots(self, args):
        "Completions for the 'takeshots' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])


    def complete_genfrom(self, args):
        "Completions for the 'use' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1]
                                   
    def complete_savein(self, args):
        "Completions for the 'savein' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])


    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in COMMANDS][state]
        # account for last argument ending in a space
        if RE_SPACE.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in COMMANDS:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]      
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in COMMANDS if c.startswith(cmd)] + [None]
        return results[state]

sourceLoc = Completer()
# we want to treat '/' as part of a word, so override the delimiters
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(sourceLoc.complete)
command_input = input('$ Source ')
if(command_input[-4:] == "xlsx"):
    fileName = command_input.split(' ',1)[1]
    print(fileName + " \nThis file will be used to generate the screenshots.")
else:
    fileName = ""
    print("Type an xlsx file")

targetLoc = Completer()
# we want to treat '/' as part of a word, so override the delimiters
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(targetLoc.complete)
command_input = input('$ Target')
if(command_input[6:] == "savein" and command_input[:1] = '\'): 
    saveHere = command_input.split(' ',1)[1]
    print(saveHere + " \nThe timestamped folder will be saved here.")
else:
    saveHere = ""
    print("Use savein to choose the destination")
                                   
cur_timestamp = str(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))
driver = webdriver.Chrome()
driver.maximize_window()
school_urls = []
fileName_screenshots = []
col_names=[]
loc = fileName 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
for i in range(sheet.ncols):
    col_names.append(sheet.cell_value(0, i).lower()) 
subs_1 = 'lat'
subs_2 = 'lon'
  
# using list comprehension  
# to get string with substring  
res_1 = [col_names.index(i) for i in col_names if subs_1 in i][0]
res_2 = [col_names.index(i) for i in col_names if subs_2 in i][0]
  
# printing result  
print ("All strings with given substring are with index : " + str(res_1) + " " + str(res_2))

folder = "folder_" + cur_timestamp

try:
    os.makedirs(folder)
except OSError:
    pass
os.chdir(folder)


for i in range(sheet.nrows): 
    if(sheet.cell_value(i,res_1)!='' and sheet.cell_value(i,res_2)!='' and sheet.cell_value(i,res_1)!='lat' and sheet.cell_value(i,res_2)!='lon' ):
        school_urls.append("https://www.google.com/maps?t=k&q=loc:" + str(sheet.cell_value(i, 2)) + "+"  + str(sheet.cell_value(i, 3)) )
        fileName_screenshots.append("screenshot_school_"+str(sheet.cell_value(i,0))+".png" )
        print(fileName_screenshots[i-1])
        print(school_urls[i-1])
        driver.get(school_urls[i-1])
        time.sleep(10)
        fullpage_screenshot(driver, fileName_screenshots[i-1])
 


