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

# implementation of spider that finds saves URLs on webpage that can be accessed without login

### imports
import scrapy
from ..items import CrawlerwithoutloginItem
from urllib.parse import urlparse


newURLs = []
foundURLs = []


#implement spider that crawls through webpages
class SpiderWithoutLogin(scrapy.Spider):
    name = 'withoutLogin'

    # initialize spider with start_urls through main_script.py
    def __init__(self, *args, **kwargs): 
      super(SpiderWithoutLogin, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')]


    # main method of spider
    def parse(self, response):
        items = CrawlerwithoutloginItem()

        # load urls found on webpage in list  
        newURLs.extend(response.xpath("//a/@href").extract())

        # delete elements that start with '#' because they just point to certain position on this page
        newURLs[:] = [x for x in newURLs if not x.startswith('#')]

        #only keep links that belong to initial domain
        initialRequestDomain = urlparse(response.request.url).netloc
        newURLs[:] = [x for x in newURLs if x.startswith('/') or urlparse(x).netloc == initialRequestDomain]

        # save cleaned urls in list foundURLs/URLsToVisit if not already present. Clear newURLs for next iteration
        lastIteration = len(foundURLs)

        newURLs[:] = [x for x in newURLs if not x in foundURLs]
        foundURLs.extend(newURLs)
        
        thisIteration = len(foundURLs)
        newURL = thisIteration - lastIteration

        # printing to see results
        print('#########')

        print('new urls this round')
        print(newURL)

        print('##### found urls')
        print(len(foundURLs))


        print('#########')


        # execute  method for every url found
        for x in newURLs: 
            nextLink = x
            nextLink = response.urljoin(nextLink)

            items['link'] = nextLink
            yield items

            yield scrapy.Request(nextLink, callback=self.parse, dont_filter=False)


