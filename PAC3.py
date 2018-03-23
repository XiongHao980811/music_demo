# -*- coding: utf-8 -*-  

from Crypto.Cipher import AES  
import base64  
import requests  
import json  
import codecs  
import time
import datetime
# 头部信息  
#代码参考  https://www.zhihu.com/question/36081767  知乎大佬对音乐评论的爬取
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
# 设置代理服务器  
proxies = {  
    'http:': 'http://121.232.146.184',  
    'https:': 'https://144.255.48.197'  
}  
  
 
second_param = "010001"  # 第二个参数  
# 第三个参数  
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"  
# 第四个参数  
forth_param = "0CoJUm6Qyw8W8jud"  
  
  
# 获取参数  
def get_params(page):  # page为传入页数  
    iv = "0102030405060708"  
    first_key = forth_param  
    second_key = 16 * 'F'  
    if (page == 1):  # 如果为第一页  
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'  
        h_encText = AES_encrypt(first_param, first_key, iv)  
    else:  
        offset = str((page - 1) * 20)  
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')  
        h_encText = AES_encrypt(first_param, first_key, iv)  
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText  
  
  
# 获取 encSecKey  
def get_encSecKey():  
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"  
    return encSecKey  
  


# 解密过程
def AES_encrypt(text, key, iv):  
    pad = 16 - len(text) % 16  
    text = text + pad * chr(pad)  
    encryptor = AES.new(key, AES.MODE_CBC, iv)  
    encrypt_text = encryptor.encrypt(text)  
    encrypt_text = base64.b64encode(encrypt_text)  
    return encrypt_text  
  
  
# 获得评论json数据  
def get_json(url, params, encSecKey):  
    data = {  
        "params": params,  
        "encSecKey": encSecKey  
    }  
    response = requests.post(url, headers=headers, data=data, proxies=proxies)  
    return response.content  


# 抓取热门评论，返回热评列表  
def get_hot_comments(url):  
    hot_comments_list = []  
    hot_comments_list.append("用户ID 用户昵称 评论时间 点赞总数 评论内容\n")  
    params = get_params(1)  # 第一页  
    encSecKey = get_encSecKey()  
    json_text = get_json(url, params, encSecKey)  
    json_dict = json.loads(json_text)  
    hot_comments = json_dict['hotComments']  # 热门评论  
    print("共有%d条热门评论!" % len(hot_comments))  
    for item in hot_comments:  
        comment = item['content']  # 评论内容  
        likedCount = item['likedCount']  # 点赞总数  
        comment_time = item['time']  # 评论时间(时间戳)
        time=datetime.datetime.utcfromtimestamp(comment_time/1000)
        times=time.strftime("%Y-%m-%d %H:%M:%S")
        userID = item['user']['userId']  # 评论者id
        nickname = item['user']['nickname']  # 昵称   
        comment_info = ('\n%d %s %s %d %s\n'%(userID, nickname, times, likedCount, comment)).encode('utf8')
        hot_comments_list.append(comment_info)  
    return hot_comments_list  
  
  
# 抓取某一首歌的全部评论  
def get_all_comments(url):  
    all_comments_list = []  # 存放所有评论  
    all_comments_list.append("用户ID 用户昵称 评论时间 点赞总数 评论内容\n"+'\n')  # 头部信息  
    params = get_params(1)  
    encSecKey = get_encSecKey()  
    json_text = get_json(url, params, encSecKey)  
    json_dict = json.loads(json_text)  
    comments_num = int(json_dict['total'])  
    if (comments_num % 20 == 0):  
        page = comments_num / 20  
    else:  
        page = int(comments_num / 20) + 1  
    print("共有%d页评论!" % page)  
    for i in range(page):  
        params = get_params(i + 1)  
        encSecKey = get_encSecKey()  
        json_text = get_json(url, params, encSecKey)  
        json_dict = json.loads(json_text)  
        if i == 0:  
            print("共有%d条评论!" % comments_num)  # 全部评论总数  
        for item in json_dict['comments']:  
            comment = item['content']  # 评论内容  
            likedCount = item['likedCount']  # 点赞总数  
            comment_time = item['time']  # 评论时间(时间戳)
            time=datetime.datetime.utcfromtimestamp(comment_time/1000)
            times=time.strftime("%Y-%m-%d %H:%M:%S")
            userID = item['user']['userId']  # 评论者id  
            nickname = item['user']['nickname']  # 昵称
            comment_info = ('\n%d %s %s %d %s\n'%(userID, nickname, times, likedCount, comment)).encode('utf8')
            all_comments_list.append(comment_info)
            
        print("第%d页抓取完毕!" % (i + 1))

       # all_comments_list.split(" ")
    return all_comments_list  
  
  
# 将评论写入文本文件  
def save_to_file(a, filename):
    f = open(filename, 'w')
    for i in a:
        f.write(i+'\n')
    f.close()
    print("写入文件成功!")  
  
  
if __name__ == "__main__":
    while True:
        start_time = time.time()  # 开始时间  
        song_id = input('please input song_id:')  
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token="%(song_id,)
        filename = u"%s.txt"%(song_id)  
        all_comments_list = get_all_comments(url)
        all_comments_list2 =get_hot_comments(url)   
        save_to_file(all_comments_list, filename)
        save_to_file(all_comments_list2,"hot_comment"+filename)
        end_time = time.time()  # 结束时间  
        print("程序耗时%f秒." % (end_time - start_time))
