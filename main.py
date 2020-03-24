import time

from requests import get
from bs4 import BeautifulSoup
import lxml
import re
import json
import operator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

#用seleium爬取amv分区所有视频av号，然后用request请求调取视频信息api，保存位json文件并读取
class AMV:
    def __init__(self, name, WatchrNum, DanMuNum, AVnum, owner, coin, favort, like, reply, share, pic):
        self.name = name
        self.pic = pic
        self.share = str(share)
        self.like = str(like)
        self.owner = owner
        self.coin = str(coin)
        self.reply = str(reply)
        self.favorate = str(favort)
        self.WatchNum = int(WatchrNum)
        self.DanMu = str(DanMuNum)
        self.AVnum = str(AVnum)

    def printSelf(self):
        src = self.name \
              + "\t\t\t\t\t\t\t作者：" + self.owner \
              + "\t\t\t" +'BV:'+ self.AVnum \
              + "\t\t播放量：" + str(self.WatchNum) \
              + "\t\t硬币：" + self.coin \
              + "\t\t收藏：" + self.favorate \
              + "\t点赞" + self.like \
              + '\t评论' + self.reply \
              + '\t分享' + self.share
        print(src)
        self.saveAMVIndex()

    def pritfs_amv(self):
        src = self.name \
              + "\t\t\t\t\t\t\t作者：" + self.owner \
              + "\t\t\t" + self.AVnum \
              + "\t\t播放量：" + str(self.WatchNum) \
              + "\t\t硬币：" + self.coin \
              + "\t\t收藏：" + self.favorate \
              + "\t点赞" + self.like \
              + '\t评论' + self.reply \
              + '\t分享' + self.share
        print(src)

    def Watchgetter(self):
        return self.WatchNum
    def getModel(self):
        model = {
            'AMV_name': self.name,
            'av': self.AVnum,
            'pic': self.pic,
            'owner': self.owner,
            'view': self.WatchNum,
            'coin': self.coin,
            'favorate': self.favorate,
            'like': self.like,
            'reply': self.reply,
            'share': self.share,
            'danmu': self.DanMu
        }
        return model
    def saveAMVIndex(self):
        model = {
            'AMV_name': self.name,
            'BV': self.AVnum,
            'pic': self.pic,
            'owner': self.owner,
            'view': self.WatchNum,
            'coin': self.coin,
            'favorate': self.favorate,
            'like': self.like,
            'reply': self.reply,
            'share': self.share,
            'danmu': self.DanMu
        }
        model = json.dumps(model, ensure_ascii=False)
        try:
            with open(data+'\\AMVIndex.json', 'a+', encoding='utf-8') as file:
                file.write(model + ',\n')
                file.close()
        except:
            print("保存出现问题！")

def init_driver(url):
    option = Options()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('--window-size=1366,768')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 1,
        }
    }
    option.add_experimental_option('prefs', prefs)
    chrome = webdriver.Chrome(options=option)
    chrome.get(url)
    return chrome
def getHTML(chrome):
    response = chrome.page_source
    bs = BeautifulSoup(response, 'lxml').find_all('ul', class_='vd-list mod-2')
    return bs
def getJsonData(jsons):
    global av
    try:
        data = jsons.get('data')
        name = data.get('title')  # 标题
        imgurl = data.get('pic')  # 封面链接
        stat = data.get('stat')
        av = data.get('bvid')  # av号
        shrae = stat.get('share')  # 分享数
        watch = stat.get('view')  # 播放数量
        danmu = stat.get('danmaku')  # 弹幕数量
        coin = stat.get('coin')  # 硬币数量
        owner = data.get('owner').get('name')  # 作者
        favorite = stat.get('favorite')  # 收藏
        like = stat.get('like')
        reply = stat.get('reply')
        amv = AMV(name, watch, danmu, av, owner, coin, favorite, like, reply, shrae, imgurl)
        amv.printSelf()

    except:
        model = {
            'AMV_name': av
        }
        model = json.dumps(model, ensure_ascii=False)
        try:
            with open('error.json', 'a+', encoding='utf-8') as f:
                f.write(model + ',\n')
                f.close()
        except:
            print("遇到未知错误")
def getAMVClass(num):
    global MaxAMV, data
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + num
    jsons = get(url).json()
    getJsonData(jsons)
def read_json():
    lists=list()
    with open(data+'\\AMVIndex.json',encoding='utf-8') as f:
        line = f.readline()
        while line:
            line = str(line).replace('[', '').replace('\n', '').replace(']', '')
            line = line.rstrip(',').strip('[').strip(']')
            print(line)
            try:
                av_json = json.loads(line)
                title = av_json.get('AMV_name')
                view = av_json.get('view')
                coin = av_json.get('coin')
                owner = av_json.get('owner')
                favorate = av_json.get('favorate')
                like = av_json.get('lke')
                reply = av_json.get('reply')
                av = av_json.get('av')
                pic = av_json.get('pic')
                share = av_json.get('share')
                try:
                    dm = av_json.get('danmu')
                except:
                    dm = 0
                amv = AMV(title, view, dm, av, owner, coin, favorate, like, reply, share, pic)
                lists.append(amv)
            except:
                print(line)
            finally:
                line = f.readline()
        f.close()
    cmpfun = operator.attrgetter('WatchNum')
    lists=sorted(lists,key=cmpfun, reverse=True)
    time.sleep(0.5)
    j = 0
    rank = path+'\\Rank'
    if not os.path.exists(rank):
        os.mkdir(rank)
    print("共计" + str(len(lists)))
    with open(rank+'\\No100.json', 'w+', encoding='utf-8') as fs:
        fs.write('[')
        try:
            for i in lists:
                j += 1
                if j <= 100:
                    i.pritfs_amv()
                    model=i.getModel()
                    model = json.dumps(model, ensure_ascii=False)
                    fs.write(model+','+'\n')
                else:
                    break
        except :
            print("出错！")
        fs.write(']')
        fs.close()

path=os.getcwd()
data=path+'\\Data'
if not os.path.exists(data):#创建数据文件夹
    os.mkdir(data)
with open(data+'\\AMVIndex.json', 'a+', encoding='utf-8') as file:#读写json
    file.write('[')
    file.close()
flag = True
last = 223159#随便给个值保证第一次能顺利运行就行
chrome = None
yeMa = open('yeMa.text', 'a+')
yeMa.close()
with open('error.json', 'a+', encoding='utf-8') as f:
    f.write('[')
    f.close()
yeMa = open('yeMa.text')
try:
    a = int(yeMa.read())
    this_num = a
except :
    this_num=1
global av
yeMa.close()
try:
    while this_num <= last:
        with open('yeMa.text', 'w', encoding='utf-8') as yeMa:
            yeMa.write(str(this_num))
            yeMa.close()
        try:
            url = 'https://www.bilibili.com/v/douga/mad/#/all/default/0/' + str(this_num) + '/'
            if flag:
                chrome = init_driver(url)
                flag = False
                # 获取当前总页数
                bs = BeautifulSoup(chrome.page_source, 'lxml')
                j = bs.find_all('li', class_='page-item last')
                for i in j:
                    last = int(i.get_text())
            else:
                chrome.get(url)
                print("第" + str(this_num) + "页")
                time.sleep(2)
            bs = BeautifulSoup(str(getHTML(chrome)), 'lxml')
            amv = bs.find_all('li')
            for b in amv:
                    try:
                        lxm = BeautifulSoup(str(b), 'lxml')
                        name = lxm.p.text
                        avUrl = lxm.a.get('href')
                        av_list = re.findall(r'(?<=\bBV)\w+\b', avUrl,re.I)
                        av = ''.join(av_list)
                        getAMVClass(av)
                    except :
                        print("有地方出错!")
        except :
            print("当前页码"+str(this_num)+"页")
            print("出现错误")
        finally:
                this_num += 1
                # 每200次请求重新打开一次chrome以防止内存爆炸
                if this_num % 200 == 0:
                    chrome.quit()
                    flag = True

finally:
    with open(data+'\\AMVIndex.json', 'a+', encoding='utf-8') as file:
        file.write(']')
        file.close()
    chrome.quit()
    with open('error.json', 'a+', encoding='utf-8') as f:
        f.write(']')
        f.close()
    print("目前数据中播放最多的是")
    MaxAMV.printSelf()
    print(this_num)
read_json()
with open ('test.txt','w+',encoding='utf-8') as f:
    f.write('0')
    f.close()


