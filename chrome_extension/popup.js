// Copyright (c) 2022 Markus Scholz

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// logic of the Google Chrome web extension

let button = document.getElementById("button")
let port = null;
let activeTab


// on click connect extension with python script and send URL of current tab
button.addEventListener('click', () => {
        // get url of open browser tab
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
            activeTab = tabs[0].url;
        });

        // connect/start main_script.py with respective URL 
        port = chrome.runtime.connectNative('com.aifb.startcrawler');
        port.postMessage(activeTab);

        port.onDisconnect.addListener(function() {
            if (chrome.runtime.lastError){
                console.log(chrome.runtime.lastError);
            }
          });
    }
)



