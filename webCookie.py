#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests,time,os

class webCooikie:
    headers=None
    UserAgent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    Referer=''
    cookies={}
    res=None
    session=None
    cookieFile='web.m'

    def __init__(self,cookieFile='web.m'):
        self.cookieFile=cookieFile
        self.session=requests.session()

    def getTime(self):
        return str(time.time()).split('.')[0]

    def getHeaders(self):
        return {
            'User-Agent': self.UserAgent,
            'Referer': self.Referer,
        }

    def loadCookie(self,cookieStr):
        cdata={i.split('=')[0]:i.split('=')[1] for i in cookieStr.split('; ')}
        self.setCookieFromDic(cdata)
        self.session.headers.update({'Cookie':cookieStr})

    def loadCookieFromFile(self,path):
        with open(path,'r') as f:
            strs=f.read()
            self.loadCookie(strs)
            f.close()

    def get(self,url,timeout=5,tryTimes=5):
        while tryTimes>0:
            try:
                tryTimes = tryTimes - 1
                res = self.session.get(url,headers=self.getHeaders(), proxies='',timeout=timeout)
                self.Referer=url
                self.refresh(res)
                return res
            except:
                pass


    def post(self,url,data,timeout=5,tryTimes=5):
        while tryTimes>0:
            try:
                tryTimes = tryTimes - 1
                res = self.session.post(url,data,headers=self.getHeaders(), proxies='',timeout=timeout)
                self.Referer=url
                self.refresh(res)
                return res
            except:
                pass


    def down(self,url,fileName=None,save_path=None,save_base='data/'):

        if save_path==None:
            save_path='/'.join(url.split('/')[2:])
            save_path=save_path.split('?')[0]
            fileName=save_path.split('/')[-1:][0]
            save_path=save_path.replace(fileName,'').replace('.','-')
        if not os.path.exists(save_base+save_path):
            os.makedirs(save_base+save_path)
        self.res = res = self.session.get(url, stream=True, headers=self.getHeaders())
        fullName=save_base+save_path+'/'+fileName
        f = open(fullName, "wb")
        downIndex=1
        for chunk in res.iter_content(chunk_size=5120):
            if chunk:
                f.write(chunk)
            downIndex=downIndex+1
        self.Referer = url
        self.refresh(res)
        return fullName

    def upload(self,url,files,data={},timeout=5,tryTimes=5):
        while tryTimes>0:
            try:
                tryTimes = tryTimes - 1
                res = self.session.post(url, data, files=files,headers=self.getHeaders(),timeout=timeout)
                self.Referer = url
                self.refresh(res)
                return res
            except:
                pass


    def setCookieFromDic(self,dic):
        if len(dic)==0:
            return 0
        for k,v in dic.items():
            if k not in self.cookies.keys():
                self.cookies[k]=v

    def refresh(self,res):
        c=requests.utils.dict_from_cookiejar(res.cookies)
        self.setCookieFromDic(c)
        self.saveCookie()

    def saveCookie(self):
        cookieArr=[]
        for k,v in self.cookies.items():
            cookieArr.append('{}={}'.format(k,v))
        with open(self.cookieFile,'w') as f:
            f.write('; '.join(cookieArr))
            f.close()

    def __del__(self):
        pass