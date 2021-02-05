from requests import get
from bs4 import BeautifulSoup
# from urllib.parse import urljoin
import time
import sys
import yagmail
from re import compile
from datetime import datetime, timedelta


time_utc = datetime.utcnow()
time_peking = (time_utc + timedelta(hours=8))
now_day = time_peking.strftime("%Y-%m-%d")
now_time = time_peking.strftime("%H:%M:%S")


def air():
    url = 'https://aqicn.org/snapshot/zibo'  # zibo_pm2.5
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.find(name='meta', attrs={'property': 'og:image'})
    png_url = s['content']
    r = get(png_url, headers={'User-Agent': ua})
    content = r.content
    with open('air.png', 'wb') as fp:
        fp.write(content)


def ge_spider():  # graduate school news
    news_list = []
    url1 = 'https://ge.sues.edu.cn/19716/list.htm'  # postgraduate school
    url2 = 'https://lib.sues.edu.cn/'  # library
    url_list = [url1, url2]
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    for i in url_list:
        response = get(i, headers={'User-Agent': ua})
        data = response.content.decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        s = soup.findAll('li', class_=compile(r"news n(.*)"))
        for item in s:
            title = '★' + item.find('a', href=compile(r'(\w)'))['title'] + '★'
            # s_link = item.find('a', href=compile(r'(\w)'))['href']
            # link = urljoin(i, s_link)
            date = item.find('span', class_="news_meta").text
            no_update = True
            if date == now_day:
                news_list.append(title)
    return news_list


def school_spider():  # report news
    news_list = []
    url1 = 'https://www.sues.edu.cn/xsbg/list.htm'  # 学术报告
    url2 = 'https://www.sues.edu.cn/17467/list.htm'  # 科研通知
    url3 = 'https://www.sues.edu.cn/17466/list.htm'  # 教学通知
    url4 = 'https://www.sues.edu.cn/17465/list.htm'  # 学校公告
    url5 = 'https://www.sues.edu.cn/xxyw/list.htm'  # 学校要闻
    url6 = 'https://www.sues.edu.cn/xykx/list.htm'  # 校园快讯
    url7 = 'https://www.sues.edu.cn/17468/list.htm'  # 官方微信
    url8 = 'https://www.sues.edu.cn/mtjj/list.htm'  # 媒体聚焦
    url9 = 'https://www.sues.edu.cn/17469/list.htm'  # 学校校报
    url10 = 'https://www.sues.edu.cn/82/list.htm'  # 学科建设
    for i in range(1, 11):
        url = eval('url%s' % i)
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
        response = get(url, headers={'User-Agent': ua})
        data = response.content.decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        s = soup.findAll('a', class_=compile(r"column-news-item item-(.?) clearfix"))
        for item in s:
            title = item.find('span', class_='column-news-title').text
            # link = urljoin(url, item['href'])
            date = item.find('span', class_='column-news-date news-date-hide').text
            if date == now_day:
                news_list.append(title)
    return news_list


def fashion_spider():
    news_list = []
    url = 'https://cfd.sues.edu.cn/'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
    response = get(url, headers={'User-Agent': ua})
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.findAll(name='td', attrs={'align': 'left', 'width': None})
    d = soup.findAll(name='td', attrs={'align': 'left', 'width': "30px"})
    date_list = []
    date_counter = 0
    for item in d:
        date_list.append(item.text)
    for item in s:
        title = item.find(name='a', href=compile(r'(\w)'))['title']
        s_link = item.find('a', href=compile(r'(\w)'))['href']
        # link = urljoin(url, s_link)
        date = date_list[date_counter]
        date_counter += 1
        if date == now_day:
            news_list.append(title)
    return news_list


def send_email(title, _contents):
    yag = yagmail.SMTP(user='suesedu@aliyun.com', password=sys.argv[2],
                       host='smtp.aliyun.com')
    send_contents = _contents
    yag.send(sys.argv[1], title, send_contents)
    print("邮件发送成功")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(r'News_Archive.txt', 'a+', encoding='utf-8') as f:
        news_1 = ge_spider()
        news_2 = school_spider()
        news_3 = fashion_spider()
        if len(news_1) != 0:
            f.write("研究生处新闻\n")
            for idx, i in enumerate(news_1):
                f.write(str(idx+1) + ". " + i + "\n")
        if len(news_2) != 0:
            f.write("学校新闻\n")
            for idx, i in enumerate(news_2):
                f.write(str(idx+1) + ". " + i + "\n")
        if len(news_3) != 0:
            f.write("学校新闻\n")
            news_3 = fashion_spider()
            for idx, i in enumerate(news_3):
                f.write(str(idx+1) + ". " + i + "\n")
        f.seek(0, 0)
        contents = [
            yagmail.inline('air.png'),
            '/n',
            f.read(),
            '\n\ngrab time: ',
            now_time,
            '\n\npowered by https://foxsun2020.github.io'
        ]
        send_email(f"{now_day}新闻", contents)
