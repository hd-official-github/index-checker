from bs4 import BeautifulSoup
import pandas as pd
import requests
from PyQt5.QtWidgets import QApplication
import urllib.parse
import urllib3 as lib3


class Exec:
    def __init__(self) -> None:
        pass

    def read_csv(self, csv):
        df = pd.read_csv(csv)
        df.dropna(subset=['livelink'], inplace=True)
        return df

    def read_csv_len(csv):
        df = pd.read_csv(csv)
        df.dropna(subset=['livelink'], inplace=True)
        return df.shape[0]

    def run_csv(self, csv, apikeys):
        df = self.read_csv(csv)
        index = 0
        keys = ""
        for i, row in df.iterrows():
            if len(apikeys):
                keys = apikeys[index]
                if len(apikeys)-1 == index:
                    index = 0
                else:
                    index += 1
                livelink = row['livelink']
                response = self.runner(livelink, keys)
                print(" livelink ",row['livelink']," response ",response)
                if response:
                    df.loc[i, 'index_status'] = 'INDEXED'
                else:
                    df.loc[i, 'index_status'] = 'NOT INDEXED'
                
                if response == "failed":
                    df.loc[i, 'index_status'] = 'FAILED TO CHECK'
                    
                df.to_csv(csv, index=False)
                yield i

            else:
                break
            # break

    def url_parse(self, url):
        rll = urllib.parse.unquote(url)
        url = urllib.parse.quote(rll)
        return url

    def runner(self, livelink, apikey):
        print("apikey ", apikey)
        irl = self.url_parse(livelink)
        r = requests.get(
            url='https://api.scraperapi.com?api_key='+apikey+'&url=https://www.google.com/search?q=site:'+irl)
        soup = BeautifulSoup(r.text, "html.parser")
        tag = soup.body
        # print(soup.body)
        st = False
        if tag is None:
            return "failed"
        
        for string in tag.strings:
            if "Try different keywords" in string:
                st = False
                break
            else:
                st = True

        return st
        # proxy = lib3.ProxyManager()
        # try:
        #     http = lib3.ProxyManager("http://"+f'{proxlink}')
        #     url = 'https://google.com/search?q='+livelink
        #     res = http.request('GET',url)
        #     # res=requests.get(url)
        #     print(res._body)
        #     # passw
        #     soup = BeautifulSoup(res._body, "html.parser")
        #     tag = soup.body
        #     st = False
        #     for string in tag.strings:
        #         # print(string)
        #         if "Try different keywords" in string:
        #             st = False
        #             break
        #         else:
        #             st = True

        #     return st
        # except Exception as e:
        #     print("ERR ",e)


if __name__ == '__main__':
    # v = Exec()
    # l = v.run_csv('sample.csv')
    app = QApplication([])
    from ui import MainWindow
    window = MainWindow()
    app.exec()
