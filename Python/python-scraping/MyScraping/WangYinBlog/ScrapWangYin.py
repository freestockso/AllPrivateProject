from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class ScrapWangYin():
    def __init__(self, scrapUrl = r"http://www.yinwang.org/blog-cn/2015/11/21/programming-philosophy"):
        self.sourceURL = scrapUrl

        moduleFile = open('WebpageModule.html', 'rt', encoding = 'UTF-8')
        self.pageModule = moduleFile.read()
        moduleFile.close()

        cssFile = open('wangYin.css', 'rt', encoding = 'UTF-8')
        self.cssModule = cssFile.read()
        cssFile.close()

    def ScrapHtml(self):
        html = urlopen(self.sourceURL)
        bsObj = BeautifulSoup(html, "html.parser")

        webTitle = bsObj.find("title")
        webBody = bsObj.find("body")

        artDate = re.search(r'\d{4}\/\d{2}\/\d{2}', self.sourceURL).group(0).replace(r'/','-')
        fileName = "r:\\(%s)%s_by王垠.html" % (artDate, webTitle.get_text())

        if webBody.find("blockquote") is not None:
            webBody.find("blockquote").replace_with("")

        scrapHtml = self.pageModule.replace("<!--@style-->", self.cssModule)
        scrapHtml = scrapHtml.replace("<!--@title-->", repr(webTitle))
        scrapHtml = scrapHtml.replace("@origUrl", self.sourceURL)
        scrapHtml = scrapHtml.replace("<!--@body-->", repr(webBody))
        scrapHtml = scrapHtml.replace("<pre><code></code></pre>", "")

        fileOutput = open(fileName, 'wt', encoding = 'UTF-8')
        fileOutput.write(scrapHtml)
        fileOutput.close()


'''
http://www.yinwang.org/blog-cn/2015/11/21/programming-philosophy
'''
