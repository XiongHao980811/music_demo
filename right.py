# encoding=utf8
import requests
from bs4 import BeautifulSoup
import os, json
import base64
from Crypto.Cipher import AES
from prettytable import PrettyTable
import warnings

warnings.filterwarnings("ignore")
BASE_URL = 'http://music.163.com/'
_session = requests.session()
# 要匹配大于多少评论数的歌曲
COMMENT_COUNT_LET = 50000

class Song(object):
    def __lt__(self, other):
        return self.commentCount > other.commentCount


# 由于网易云音乐歌曲评论采取AJAX填充的方式所以在HTML上爬不到，需要调用评论API，而API进行了加密处理，下面是相关解决的方法
def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


# 通过第三方渠道获取网云音乐的所有歌曲ID
# 这里偷了个懒直接从http://grri94kmi4.app.tianmaying.com/songs爬了，这哥们已经把官网的歌曲都爬过来了，省事不少
def getSongIdListBy3Party():
    pageMax = 1  # 要爬的页数，可以根据需求选择性设置页数
    songIdList = []
    for page in range(pageMax):
        url = 'http://grri94kmi4.app.tianmaying.com/songs?page=' + str(page)
        # print url
        url.decode('utf-8')
        soup = BeautifulSoup(_session.get(url).content)
        # print soup
        aList = soup.findAll('a', attrs={'target': '_blank'})
        for a in aList:
            songId = a['href'].split('=')[1]
            songIdList.append(songId)
    return songIdList


# 从官网的 发现-> 歌单 页面爬取网云音乐的所有歌曲ID
def getSongIdList():
    pageMax = 1  
    songIdList = []
    for i in range(1, pageMax + 1):
        url = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=' + str(i * 35)
        url.decode('utf-8')
        soup = BeautifulSoup(_session.get(url).content)
        aList = soup.findAll('a', attrs={'class': 'tit f-thide s-fc0'})
        for a in aList:
            uri = a['href']
            playListUrl = BASE_URL + uri[1:]
            soup = BeautifulSoup(_session.get(playListUrl).content)
            ul = soup.find('ul', attrs={'class': 'f-hide'})
            for li in ul.findAll('li'):
                songId = (li.find('a'))['href'].split('=')[1]
                print '爬取歌曲ID成功 -> ' + songId
                songIdList.append(songId)
    # 歌单里难免有重复的歌曲，去一下重复的歌曲ID
    songIdList = list(set(songIdList))
    return songIdList


# 匹配歌曲的评论数是否符合要求
# let 评论数大于值
def matchSong(songId, let):
    url = BASE_URL + 'weapi/v1/resource/comments/R_SO_4_' + str(songId) + '/?csrf_token='
    headers = {  
    'Host': "music.163.com",  
    'Accept-Language': "zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4",  
    'Accept-Encoding': "gzip, deflate",  
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "vjuids=d5d34c2e.15ae7578bfa.0.55c4265b9584f; _ntes_nnid=7c9123c588eb2681e57d9416193550a7,1489939959315; _ntes_nuid=7c9123c588eb2681e57d9416193550a7; vinfo_n_f_l_n3=86353b298a14c5a8.1.0.1489939959688.0.1489940092331; usertrack=c+5+hVkIB7uB5m9xJyc5Ag==; _ga=GA1.2.670961798.1493698506; vjlast=1489939959.1507595594.23; __gads=ID=7fce77699f603ad2:T=1507595596:S=ALNI_Mbuc92aibtJ7PjOcB3x6sdgWUCNKg; jsessionid-cpta=3VfyAmh5TN6ARRGZ41corzGOoQZ%2BSZcCCClkbPaTbb7P8jN0X0TGTPLSxMMVHgSJ8gQ%5Co9jLTi%2FnovUVuouMNNlz4yjdnLMVOZmSVFkn9DQeOcQmR0q8z%2FmBEBzY2n4Q%5CiPBoef5XH1kVD8NEGl%2FNdZ7atUtFNFxXcpTfycVHfIWYJrU%3A1507606347815; c98xpt_=30; NETEASE_WDA_UID=603393554#|#1507605464937; JSESSIONID-WYYY=s6V%5CEYJiUY6OpUHpCFnPJrjNv7mVOwurRz8qfrm3UYOBjNKpwt6KhFVAOrsG1nFqUA%5CnOX4iTIpwkFxJ6EQV%2Fb8Yyhh%2FaxUNYiUW1wE%2FX%2BQA7F%5CVwOrWt%2FWVF%2FjUxjZUcViUtSh8%2BGjHVKMTXeXDAgDzV8r1QygjAUIkmRFx%2BMuQW1Kp%3A1510118420823; _iuqxldmzr_=32; __utma=94650624.670961798.1493698506.1510111148.1510116621.23; __utmb=94650624.4.10.1510116621; __utmc=94650624; __utmz=94650624.1506566608.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; MUSIC_U=cd9cf148c04198232ad668812858aa50fe981050025ee7d78969173f4660225309fe5abad8d27f1eb94085d872358d065ca7f8b5c996b23176bdb7494e206a46a961a7d0df0fad0cc3061cd18d77b7a0; __remember_me=true; __csrf=63aa830c46f784b91b650ff5b55d37a4",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3226.400 QQBrowser/9.6.11681.400",
    'Connection': "keep-alive",
    'Referer': 'http://music.163.com/'  
} 
    text = {'username': '', 'password': '', 'rememberLogin': 'true'}
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    req = requests.post(url, headers=headers, data=data)
    total = req.json()['total']
    if int(total) > let:
        song = Song()
        song.id = songId
        song.commentCount = total
        return song


# 设置歌曲的信息
def setSongInfo(song):
    url = BASE_URL + 'song?id=' + str(song.id)
    url.decode('utf-8')
    soup = BeautifulSoup(_session.get(url).content)
    strArr = soup.title.string.split(' - ')
    song.singer = strArr[1].encode('gbk', 'ignore')
    song.name = strArr[0].encode('gbk', 'ignore')
    # 去除歌曲名称后面（）内的字，如果不想去除可以注掉下面三行代码
    index = name.find('（')
    if index > 0:
        name = name[0:index]
    song.name = name


# 获取符合条件的歌曲列表
def getSongList():
    print ' ##正在爬取歌曲编号... ##'
    # songIdList = getSongIdList()
    songIdList = getSongIdListBy3Party()
    print ' ##爬取歌曲编号完成，共计爬取到' + str(len(songIdList)) + '首##'
    songList = []
    print ' ##正在爬取符合评论数大于' + str(COMMENT_COUNT_LET) + '的歌曲... ##'
    for id in songIdList:
        song = matchSong(id, COMMENT_COUNT_LET)
        if None != song:
            setSongInfo(song)
            songList.append(song)
            ##print song.id
            print '成功匹配一首{名称:', song.name , '-', song.singer, ',评论数:', song.commentCount,u',歌曲ID:', song.id, '}'
    print ' ##爬取完成，符合条件的的共计' + str(len(songList)) + '首##'
    return songList


def main():
    songList = getSongList()
    # 按评论数从高往低排序
    songList.sort()
    # 打印结果
    table = PrettyTable([u'排名', u'评论数', u'歌曲名称', u'歌手',u'歌曲ID'])
    for index, song in enumerate(songList):
        table.add_row([index + 1, song.commentCount, song.name, song.singer, song.id])
    print table
    print 'End'


if __name__ == '__main__':
    main()
