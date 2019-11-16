try:
    import json
    import itertools
    import uuid
    import sys
    import requests
    import os
    import pandas as pd
    import datetime
    from bs4 import BeautifulSoup
except Exception as e:
    print("Some Modules are Missings ")


class BaseUrl(object):
    def __init__(self, Query=''):
        self.url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch"
        self.__query = Query
        self.baseurl = self.url % self.__query
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        print(self.baseurl)


class WebCrawler(object):
    def __init__(self, Query, numberImage=100):
        self.maxImage = numberImage
        self.query = Query
        self.baseurl = BaseUrl(Query=self.query)

    def soup(self):
        response = requests.get(self.baseurl.baseurl, headers=self.baseurl.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def getImageURl(self):

        if (self.maxImage >100):
            print("Number of Images cannot exceeds 100")
        else:
            soup = self.soup()
            image_elements = soup.find_all("div", {"class": "rg_meta"})
            metadata_dicts = (json.loads(e.text) for e in image_elements)
            link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
            return itertools.islice(link_type_records, self.maxImage)


class GoogleImageDownloader(object):
    def __init__(self, Query, numberImage=100):
        self.query = Query
        self.numofImage = numberImage
        self.crawler = WebCrawler(Query=self.query, numberImage=self.numofImage)

    def getUrls(self):
        data = self.crawler.getImageURl()
        data = [ (i, url) for i, (url, image_type) in enumerate(data) ]
        return data

    def saveCsv(self):
        data = self.getUrls()
        df = pd.DataFrame(data=data)
        df.to_csv("Result.csv")
        print("Saved on your Computer with Result.csv")

    def saveJson(self):
        data = self.getUrls()
        df = pd.DataFrame(data=data)
        df.to_json("Result.json")
        print("Saved on your Computer with Result.json")

    def downloadImages(self):

        data = self.getUrls()
        df = pd.DataFrame(data=data, columns=["No", "Url"])

        start = datetime.datetime.now()

        for i, url in enumerate(df["Url"].to_list()):

            print("Downloading Image {}\t{}".format(i, url))

            data = requests.get(url=url).content

            cwd = os.getcwd()                       # get CWD
            folder = 'Images'                         # Create Folder Logs
            newPath = os.path.join(cwd, folder)     # change Path


            try:
                """ try to create directory """
                os.mkdir(newPath)                   # create Folder

            except Exception as e:

                """ Directory already exists """

                filename = "{}.jpg".format(i)
                completePath = os.path.join(newPath, filename)

                with open(completePath, "wb") as f:
                    f.write(data)

        end = datetime.datetime.now()

        print("Total Time : {}".format(end-start))


if __name__ == "__main__":
    image = GoogleImageDownloader(Query="cat", numberImage=50)
    #print(image.getUrls())
    image.downloadImages()
