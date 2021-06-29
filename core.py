from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re, time
class Gui:
    def __init__(self):
        self.color = {"background":"#1c1c21",
                "FontH1":"#86afe8",
                "Button":"#5b87d8"
                    }
        try:
            self.publicIp = requests.get("https://api.ipify.org").text
        except:
            messagebox.showerror("SAMURAI","THE API IS OFF")
        print(self.publicIp)
        self.root = Tk()
        self.root.geometry("900x500")
        self.root["bg"] = self.color["background"]
        Label(self.root,text="Samurai", bg=self.color["background"],fg=self.color["FontH1"],font=('',30)).place(x=20,y=10)
        Button(self.root,relief="flat",highlightthickness=0,text="Scrape",command=self.scrape,bg=self.color["Button"],fg="#FFF").place(x=800,y=450)
        Button(self.root,relief="flat",highlightthickness=0,text="check",command=self.Check,bg=self.color["Button"],fg="#FFF").place(x=800,y=400)
        self.proxyWillBeHere = Text(self.root,highlightthickness=0, bg="#161a21",fg="#FFF",relief='flat',width=90)
        self.proxyWillBeHere.place(x=20,y=80)
    def scrapeUrl(self,url):
        try:
            t = "\n"
            d = requests.get(url).text
            soup = BeautifulSoup(d, features="html.parser")
            for script in soup(["script","style","td","abbr"]):
                script.extract()
            text = soup.get_text()
            for ligne in text.split("\n"):
                if(re.match("((?:1?\d{1,2}|2[0-4]\d|25[0-5])\.){3}(?:1?\d{1,2}|2[0-4]\d|25[0-5]):\d{2,5}",ligne)):
                    t += ligne + "\n"
            return t
        except:
            pass
    def GetLink(self):
        with open("links","r") as f:
            data = f.read().split("\n")
            f.close()
        return data
    def scrape(self):
        proxiLink = self.GetLink()
        proxy = ''
        for url in proxiLink:
            try:
                proxy += self.scrapeUrl(url)
            except:
                pass
        self.proxyWillBeHere.insert(INSERT, proxy)
        self.proxy = proxy
    def Show(self):
        self.root.mainloop()
    def Check(self):
        work = ""
        self.proxyWillBeHere.delete("1.0", END)
        for proxi in self.proxy.split("\n"):
            if self.CheckProxy(proxi) == self.publicIp:
                pass
            else:
                work += "\n" + proxi
            self.root.update()
            print(work)
            self.proxyWillBeHere.insert(INSERT, proxi + "\n")
    def CheckProxy(self,proxy):
        try:
            proxies = {"https":proxy}
            r = requests.get("https://api.ipify.org", proxies=proxies).text
            return r
        except:
            time.sleep(.8)
            return None
            
