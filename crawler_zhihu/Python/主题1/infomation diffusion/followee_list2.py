# -*- coding: utf-8 -*-
import requests
import re
import codecs
import json
import time
from time import sleep,ctime
import datetime
import thread
import threading



#user_list = ['shisu','wang-wei-63','allenzhang','kentzhu','yangbo','baiya','junyu','wang-xiao-chuan','wangxing','gongjun','zhouyuan','hi-id','shek','commando','chen-hao-84','jin-chen-yu','jixin','linan','raymond-wang']

user_list = ['zihaolucky']


login_data = {'email': '137552789@qq.com', 'password': 'God2241226','rememberme':'y',}




# session对象,会自动保持cookies
s = requests.session()

# auto-login.
def login(login_data):
    s.post('http://www.zhihu.com/login', login_data)


def load_more_thread1(user,data):
    # 进行加载时的Request URL
    click_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
    
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/people/' + user + '/followees',
        'Content-Type':'application/x-www-form-urlencoded',
        }
        
    # form data.
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]              # hash_id
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]                    # _xsrf
    
    # 
    load_more_times = int(re.findall('<strong>(.*?)</strong>',data)[2]) / 20
    
    
    # ---- key module ----
        # 写入头20个用户信息
    user_id = re.compile('zhihu.com/people/(.*?)"').findall(data)
    user_id = user_id[1:len(user_id)]
    answers = re.findall('answers" class="zg-link-gray-normal">(.*?) ',data)
    asks = re.findall('asks" class="zg-link-gray-normal">(.*?) ',data)
    followers = re.findall('followers" class="zg-link-gray-normal">(.*?) ',data)
    goods = re.findall('class="zg-link-gray-normal">(.*?) ',data)
    goods = goods[3:len(goods):4]
    
    fp.write('user_id,followers,asks,answers,goods')
    fp.write('\r\n')
    write_file(user_id,followers,asks,answers,goods)
        # 写入其余用户信息
    
    for i in range(1,load_more_times+1,2):
        t_start = time.localtime()[5]
        offsets = i*20
        # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        
        # debug and improve robustness. Date: 2014-02-12
        try:
            r = s.post(click_url,data=payload,headers=header_info,timeout=10)
        except:
            # 响应时间过程过长则重试
            print 'repost'
            r = s.post(click_url,data=payload,headers=header_info,timeout=60)
        
        
            # parse info.
        user_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
        user_id = user_id[0:len(user_id):5]
        user_info = re.findall('class=\\\\"zg-link-gray-normal\\\\">(.*?) ',r.text)
        followers = user_info[0:len(user_info):4]
        # print followers
        asks = followers = user_info[1:len(user_info):4]
        answers = user_info[2:len(user_info):4]
        goods = user_info[3:len(user_info):4]
        
        #print user_id,followers,asks,answers,goods
        #print len(user_id),len(followers),len(asks),len(answers),len(goods)
        
        
        write_file(user_id,followers,asks,answers,goods)
        # print user_id
        t_elapsed = time.localtime()[5] - t_start
        print 'thread#1 got:',offsets,'users.','elapsed: ',t_elapsed,'s.\n'
   




def load_more_thread2(user,data):
    # 进行加载时的Request URL
    click_url = 'http://www.zhihu.com/node/ProfileFollowersListV2'
    
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/people/' + user + '/followees',
        'Content-Type':'application/x-www-form-urlencoded',
        }
        
    # form data.
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]              # hash_id
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]                    # _xsrf
    
    # 
    load_more_times = int(re.findall('<strong>(.*?)</strong>',data)[2]) / 20
    
    
        # 写入其余用户信息
    
    for i in range(2,load_more_times+1,2):
        t_start = time.localtime()[5]
        offsets = i*20
        # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        
        # debug and improve robustness. Date: 2014-02-12
        try:
            r = s.post(click_url,data=payload,headers=header_info,timeout=10)
        except:
            # 响应时间过程过长则重试
            print 'repost'
            r = s.post(click_url,data=payload,headers=header_info,timeout=20)
        
        
            # parse info.
        user_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
        user_id = user_id[0:len(user_id):5]
        user_info = re.findall('class=\\\\"zg-link-gray-normal\\\\">(.*?) ',r.text)
        followers = user_info[0:len(user_info):4]
        asks = user_info[1:len(user_info):4]
        answers = user_info[2:len(user_info):4]
        goods = user_info[3:len(user_info):4]
        
        #print user_id,followers,asks,answers,goods
        #print len(user_id),len(followers),len(asks),len(answers),len(goods)
        
        
        write_file(user_id,followers,asks,answers,goods)
        # print user_id
        t_elapsed = time.localtime()[5] - t_start
        print 'thread#2 got:',offsets,'users.','elapsed: ',t_elapsed,'s.\n'
    
    




    
    


def main():
    # login
    s.post('http://www.zhihu.com/login', login_data)
    
    for user in user_list:
        print 'crawling ' + user + '\'s followees...\n'
        # 写文件
        global fp
        fp = codecs.open(user + '.txt', 'w', 'utf-8')
        
        url = 'http://www.zhihu.com/people/' + user + '/followees'
        # 转跳到用户followers页
        r = s.get(url)
        data = r.text
        print 'starting at:',ctime()
        threads = []
        t = threading.Thread(target=load_more_thread1,args=(user,data))
        threads.append(t)
        t = threading.Thread(target=load_more_thread2,args=(user,data))
        threads.append(t)
        
        
        # 多线程
        for i in range(2):
               threads[i].start()
        for i in range(2):
               threads[i].join()
        print 'all DONE at:',ctime()
        
        
    
def write_file(user_id,followers,asks,answers,goods):
    for i in range(len(user_id)):
        global fp
        fp.write( user_id[i].strip()+','+followers[i].strip()+','+asks[i].strip()+','+answers[i].strip()+','+goods[i].strip() )
        fp.write('\r\n')
        
    
    
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'
