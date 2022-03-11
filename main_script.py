# Copyright (c) 2022 Markus Scholz

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


### imports
import csv
import json
import struct
import subprocess
from urllib.parse import urlparse 
import sys


### methods

#receive url from extension. Implemented as seen on github page (https://github.com/mdn/webextensions-examples/blob/master/native-messaging/app/ping_pong.py)
def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode('utf-8')
    return json.loads(message)


# run scrapy spiders with respective URL
def run_spiders(URLDomainWithoutEnding):

    commandWithoutLogin = 'scrapy crawl withoutLogin -o results_' + URLDomainWithoutEnding + '_withoutLogin.csv -a start_url=' + URL
    subprocess.run(commandWithoutLogin, shell=True, cwd='crawlerWithoutLogin')

    commandWithLogin = 'scrapy crawl withLogin -o results_' + URLDomainWithoutEnding + '_withLogin.csv -a start_url=' + URL
    subprocess.run(commandWithLogin, shell=True, cwd='crawlerWithLogin')


# load results from spiders and save them into lists. removing 'link' because it's automatically added
def loading_links_from_spiders(URLDomainWithoutEnding):
    with open("crawlerWithoutLogin/results_" + URLDomainWithoutEnding + "_withoutLogin.csv", 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            linksWithoutLogin.append(str(line[0]))

    linksWithoutLogin.remove('link')

    for i, x in enumerate(linksWithoutLogin):
        linksWithoutLogin[i] = x.split('://', 1)[1]

    with open("crawlerWithLogin/results_" + URLDomainWithoutEnding + "_withLogin.csv", 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            linksWithLogin.append(str(line[0]))

    linksWithLogin.remove('link')
    for i, x in enumerate(linksWithLogin):
        linksWithLogin[i] = x.split('://', 1)[1]



# compare links found by the two spiders and write those only in withLogin into a csv file
def compareLinksFound(linksWithLogin, linksWithoutLogin):
    if set(linksWithLogin) == set(linksWithoutLogin):
        print('links are identical. no sign for login')
    else:
        print('lists are not identical. sign for login')
        print('withLogin: ' + str(len(linksWithLogin)))
        print('withoutLogin: ' + str(len(linksWithoutLogin)))
        difference = linksWithLogin
        difference[:] = [x for x in difference if not x in linksWithoutLogin]
        print(len(difference))
        print('withLogin: ' + str(len(linksWithLogin)))
        print('withoutLogin: ' + str(len(linksWithoutLogin)))
        print(difference)

        write_difference_to_csv(difference)

def write_difference_to_csv(difference):
    with open('difference.csv', 'w') as csvfile:
        for item in difference:
            csvfile.write(item + '\n')


### program
URL = str(getMessage())
print(URL)
URLDomainWithoutEnding = urlparse(URL).netloc.split(".")[1]


linksWithoutLogin = []
linksWithLogin = []
difference = []


run_spiders(URLDomainWithoutEnding)
loading_links_from_spiders(URLDomainWithoutEnding)
compareLinksFound(linksWithLogin, linksWithoutLogin)
