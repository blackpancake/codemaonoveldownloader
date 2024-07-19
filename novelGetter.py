import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox as mBox
import json
import time
import random
import re
import html
import threading
import math
import io
import sys

import requests
from requests.adapters import HTTPAdapter

import loading_window

def GETPATH(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径

    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

SESS = requests.Session()
SESS.mount('http://', HTTPAdapter(max_retries=3))
SESS.mount('https://', HTTPAdapter(max_retries=3))
from PIL import Image, ImageTk


REPCHR, IPCHAR = r'[\/:*?"<>|()]+', r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$'
STATSLIST = ['未知', '连载中', '已完结', '已删除']

ages = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]


def strftime(timestamp, format_string='%Y?%m@%d$ %H:%M:%S'):
    return time.strftime(format_string, time.localtime(timestamp)).replace(
        '?', '年').replace('@', '月').replace('$', '日')


def rdags():
    return {'User-Agent': random.choice(ages), 'Connection': 'close'}


def formt(title, texthtm):
    return '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{}</title>
<link rel="shortcut icon" href="https://static.codemao.cn/community_frontend/favicon.ico">
</head>
<body bgcolor="#fffcf6">
{}
</body>
</html>'''.format(title, texthtm).replace('↵', '')


def formtTXT(title, texthtm):
    return title + '\n\n' + html.unescape(
        re.sub(r'<.*?>', '',
               texthtm.replace('↵', '').replace('<hr />', '————' * 20).replace('<br />', '\n').replace('<br/>', '\n')))


class novel:
    def __init__(self, number, ip, port):
        self.dl_ip = ip
        self.dl_port = port
        self.number = str(number)
        self.cover = 'https://shequ.codemao.cn/wiki/novel/cover/' + self.number
        try:
            self.info = SESS.get('https://api.codemao.cn/api/fanfic/' +
                                     self.number,
                                     headers=rdags(),
                                     proxies=self.rdip(),
                                     timeout=1.5)
        except Exception as F:
            raise TabError(F)
        self.cover_json = json.loads(self.info.text)

        self.not_fd = "error_code" in self.cover_json or self.cover_json[
            'code'] != 200
        if self.not_fd:
            self.id = None
            return
        self.realjson = self.cover_json['data']
        self.cover_json = self.cover_json['data']["fanficInfo"]
        self.id = self.cover_json['id']
        self.novel_name = self.cover_json['title']
        self.fm_url = self.cover_json['cover_pic']

        self.isghost = "cdn-community.codemao.cn" not in self.fm_url and "static.codemao.cn" not in self.fm_url
        try:
            self.picdata = SESS.get(self.fm_url,
                                        headers=rdags(),
                                        proxies=self.rdip(),
                                        timeout=1.5).content
        except Exception as F:
            # raise TabError(F)
            pass
        self.intrde = self.cover_json["introduction"] if self.cover_json[
            "introduction"] != '' else '暂无简介'
        self.stats = STATSLIST[self.cover_json["status"]]
        self.cover_pic_url = self.cover_json["cover_pic"]
        self.view_times = self.cover_json["view_times"]
        self.collect_times = self.cover_json["collect_times"]
        self.fanfic_type_name = self.cover_json["fanfic_type_name"]
        self.create_time = self.cover_json["create_time"]
        self.create_date = strftime(self.create_time)
        self.update_time = self.cover_json["update_time"]
        self.update_date = strftime(self.update_time)
        self.author_uid = self.cover_json["user_id"]
        self.author_name = self.cover_json["nickname"]
        self.total_words = self.cover_json["total_words"]
        self.cptrs = self.realjson["sectionList"]
        self.total_infoA = '''==================书籍信息==================
书名：{novel_name}
作者：{nickname}
作者uid：{uid}
书籍简介：{intd}
更新状态：{stats}
浏览量：{vtimes}次
收藏量：{ctimes}次
收藏率：{wptm:.2%}
小说分类：{type}
创建时间：{cdate}
最后一次更新时间：{udate}
总字数：{words}字
章节数量：{lencptr}章
每章平均字数：{avrword:.1f}字
============================================'''.format(
            novel_name=self.novel_name,
            nickname=self.author_name,
            uid=self.author_uid,
            intd=self.intrde,
            stats=self.stats,
            vtimes=self.view_times,
            ctimes=self.collect_times,
            wptm=self.collect_times /
            self.view_times if self.view_times != 0 else 0,
            type=self.fanfic_type_name,
            cdate=self.create_date,
            udate=self.update_date,
            words=self.total_words,
            lencptr=len(self.cptrs),
            avrword=self.total_words / len(self.cptrs) if len(self.cptrs) != 0
            else 0) + '\n\n\n\n\n\n++++++++++++++++++章节目录++++++++++++++++++'

        for n, i in enumerate(self.cptrs):
            self.total_infoA += '''\n第{num}章——{title:　<30}[字数：{words}字 | 最后更新时间：{udate}]\n'''.format(
                num=n + 1,
                title=i['title'],
                words=i['words_num'],
                udate=strftime(i['update_time']))
        self.total_infoA += '++++++++++++++++++++++++++++++++++++++++++++'
        self.total_infoB = '''===========书籍信息===========
书名：{novel_name}
作者：{nickname}
作者uid：{uid}
书籍简介：{intd}
更新状态：{stats}
浏览量：{vtimes}次
收藏量：{ctimes}次
收藏率：{wptm:.2%}
小说分类：{type}
创建时间：{cdate}
最后一次更新时间：{udate}
总字数：{words}字
章节数量：{lencptr}章
每章平均字数：{avrword:.1f}字
=============================='''.format(
            novel_name=self.novel_name,
            nickname=self.author_name,
            uid=self.author_uid,
            intd=self.intrde,
            stats=self.stats,
            vtimes=self.view_times,
            ctimes=self.collect_times,
            wptm=self.collect_times /
            self.view_times if self.view_times != 0 else 0,
            type=self.fanfic_type_name,
            cdate=self.create_date,
            udate=self.update_date,
            words=self.total_words,
            lencptr=len(self.cptrs),
            avrword=self.total_words /
            len(self.cptrs) if len(self.cptrs) != 0 else 0)

    def rdip(self):
        assert self.dl_port is not None and self.dl_ip is not None or self.dl_port is self.dl_ip is None
        if self.dl_port is not None and self.dl_ip is not None:
            return {'https': 'https://{}:{}'.format(self.dl_ip, self.dl_port)}
        else:
            return {'http': 'http://{}:{}'.format(self.dl_ip, self.dl_port)}

    def summon_dir(self, path='.'):
        self.dir_name = '{author}-《{book}》'.format(author=self.author_name,
                                                   book=self.novel_name)
        self.dir_path = os.path.join(path, self.dir_name)
        try:
            os.mkdir(self.dir_path)
        except FileExistsError:
            raise FileExistsError
        with open(os.path.join(self.dir_path, '书籍信息.txt'),
                  'w+',
                  encoding='utf-8') as f:
            f.write(self.total_infoA)

    def save_each_cptr(self, ashtml=True, astxt=False):
        try:
            if ashtml:
                os.mkdir(os.path.join(self.dir_path, 'HTML格式'))
            if astxt:
                os.mkdir(os.path.join(self.dir_path, 'TXT格式'))
        except FileExistsError:
            raise FileExistsError

        for n, i in enumerate(self.cptrs):
            this_cptr = SESS.get(
                'https://api.codemao.cn/api/fanfic/section/' + str(i['id']),
                headers=rdags(),
                proxies=self.rdip(),
                timeout=1.5)
            this_json = json.loads(this_cptr.text)
            not_fd = "error_code" in this_json or this_json['code'] != 200
            if not_fd:
                continue
            this_json = this_json["data"]["section"]
            if ashtml:
                with open(os.path.join(
                        self.dir_path, 'HTML格式', '{}-{}.html'.format(
                            n + 1, re.sub(REPCHR, '', this_json['title']))),
                          'w+',
                          encoding='utf-8') as f:
                    f.write(formt(i['title'], this_json["content"]))
            if astxt:
                with open(os.path.join(
                        self.dir_path, 'TXT格式', '{}-{}.txt'.format(
                            n + 1, re.sub(REPCHR, '', this_json['title']))),
                          'w+',
                          encoding='utf-8') as f:
                    f.write(formtTXT(i['title'], this_json["content"]))
            jd = math.floor(n / len(self.cptrs) * 100)
            assert jd <= 100
            yield jd
        yield 100

    def save_fm(self, filepth=None):
        if filepth is None:
            filepth = os.path.join(self.dir_path, '封面.jpg')
        with open(filepth, 'wb+') as f:
            f.write(self.picdata)


######################################GUI##############################################
class ToolTip(object):
    ptvavlx = ptvavly = 20

    def __init__(self, widget):
        self.widget = widget
        self.DEAD = True

    def showtip(self, text):
        """Display text in tooltip window"""
        self.DEAD = False
        x = self.widget.winfo_rootx() + self.ptvavlx
        y = self.widget.winfo_rooty() + self.ptvavly
        self.tw = tk.Toplevel(self.widget)
        self.tw.overrideredirect(1)
        self.tw.geometry("+%d+%d" % (x, y))
        self.label = tk.Label(self.tw,
                              text=text,
                              justify=tk.LEFT,
                              background="#fffff4",
                              relief=tk.SOLID,
                              borderwidth=1,
                              font=("宋体", "9", "normal"))
        self.label.pack()

    def hidetip(self):
        self.DEAD = True
        self.label.destroy()
        self.tw.destroy()

    def move(self, event=None):
        if not self.DEAD:
            self.tw.wm_geometry("+%d+%d" %
                                (event.x_root + 10, event.y_root + 10))


def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        assert toolTip.DEAD
        toolTip.showtip(text)

    def leave(event):
        assert not toolTip.DEAD
        toolTip.hidetip()

    def move(event):
        toolTip.move(event)

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    widget.bind('<Motion>', move)


class App:
    def __init__(self):
        self.body = tk.Tk()
        self.body.title('编程猫小说爬取器')
        self.body.geometry('850x430')
        self.body.resizable(0, 0)
        self.body.protocol("WM_DELETE_WINDOW", self.when_close)
        self.body.iconbitmap(GETPATH("assets/ke.ico"))
        self.isdowning = False
        self.novel = self.dl_ip = self.dl_port = None
        # define
        self.styles = ttk.Style()
        self.styles.configure("My.TLabel", font=('黑体', '13'))
        self.styles.configure("My2.TLabel", font=('宋体', '10'))
        self.styles.configure("My.TEntry", font=('宋体', '10'))
        self.styles.configure("My.TButton", font=('宋体', '11'))
        self.styles.configure("My.TLabelFrame", font=('宋体', '10'))
        self.styles.configure("SmallTip.TLabel",
                              font=('宋体', '11'),
                              foreground='#FF6600')
        self.styles.configure("Link.TLabel",
                              font=('宋体', '10'),
                              foreground='#0000FF')

        self.uid_tip = ttk.Label(self.body,
                                 style="My.TLabel",
                                 text='输入你要爬取的小说的uid号：')
        self.uid_ety = ttk.Entry(self.body)
        self.intrde_txt = scrolledtext.ScrolledText(self.body,
                                                    width=30,
                                                    height=23,
                                                    relief=tk.SOLID)
        self.itnd_tip = ttk.Label(self.body, style="My2.TLabel", text='小说信息：')
        createToolTip(self.itnd_tip, '小说的浏览量、作者、字数等信息')
        self.go_btn = ttk.Button(self.body,
                                 style="My.TButton",
                                 text='选定小说',
                                 command=self.get_info)
        createToolTip(self.go_btn, '获取并展示小说的浏览量、作者和章节目录等信息，\n爬取正文前要先选定')
        self.type_tip = ttk.Label(self.body,
                                  style="My2.TLabel",
                                  text='正文保存格式：')
        createToolTip(self.type_tip, '爬取到的小说正文有两种格式保存，\n至少选择一个（可多选）')

        self.frame1 = ttk.LabelFrame(self.body, text='章节目录')
        self.cptrlist = scrolledtext.ScrolledText(self.frame1, relief=tk.SOLID)

        self.pb_lb = ttk.Label(self.body, style="My2.TLabel", text='爬取进度：')
        self.pqjdbfb = ttk.Label(self.body, style="My.TLabel", text='0%')
        self.p1 = ttk.Progressbar(self.body,
                                  length=200,
                                  mode="determinate",
                                  orient=tk.HORIZONTAL,
                                  takefocus=False)

        self.ashtml = tk.BooleanVar()
        self.html_rd = ttk.Checkbutton(self.body,
                                       text="html格式",
                                       variable=self.ashtml,
                                       command=self.Checked)
        createToolTip(
            self.html_rd,
            'html格式包含正文中的颜色、图片、大小，\n一般不可能出现排版错乱，稳定，有阅读体验，但占用空间大，\n只能用浏览器阅读。\n（不联网加载不出图片，但能看到文字）'
        )
        self.ashtml.set(True)

        self.astxt = tk.BooleanVar()
        self.txt_rd = ttk.Checkbutton(self.body,
                                      text="txt格式",
                                      variable=self.astxt,
                                      command=self.Checked)
        createToolTip(
            self.txt_rd,
            'txt格式不包含正文中的颜色、图片、大小，\n有可能出现排版错乱，但占用空间小，\n用系统的记事本就能阅读。')
        self.astxt.set(True)

        self.sb = ttk.Button(self.body,
                             style="My.TButton",
                             text='开始\n爬取',
                             command=self.download)
        createToolTip(self.sb,
                      '将小说的封面、浏览量、作者和章节目录等信息\n以及每章的正文按照你所设置的文件格式下载保存到本地')
        self.put = ttk.Button(self.body,
                              style="My.TButton",
                              text='导出信息',
                              command=self.outload)
        self.put_fm = ttk.Button(self.body,
                                 style="My.TButton",
                                 text='导出封面',
                                 command=self.outload_fm)
        createToolTip(self.put, '仅将小说的浏览量、作者、字数和章节目录等小说信息\n导出为txt到本地')
        createToolTip(self.put_fm, '仅将小说的封面导出为jpg图片到本地')
        self.now_novel = tk.Message(self.body,
                                    text='当前要爬取的小说：{}\nuid：{}'.format(
                                        '未选定', '暂无'),
                                    font=('宋体', '10'),
                                    width=178)
        self.unbtn = ttk.Button(self.body,
                                style="My.TButton",
                                text='取消\n选定',
                                command=self.unselect)
        createToolTip(self.unbtn, '点此取消选定该小说')

        self.unbtn['state'] = 'disabled'
        self.sb['state'] = 'disabled'
        self.put['state'] = 'disabled'
        self.put_fm['state'] = 'disabled'

        self.fm_tip = ttk.Label(self.body, style="My2.TLabel", text='小说封面：')
        createToolTip(self.fm_tip,
                      '小说的封面，仅此而已。\n只是预览图，可能会有形变、压缩等现象，\n但实际爬取的封面没有这些问题')
        self.fm_canvas = tk.Canvas(self.body,
                                   bg='Gray',
                                   relief=tk.SOLID,
                                   borderwidth=1)

        self.whatuid = ttk.Label(self.body,
                                 style="Link.TLabel",
                                 text='什么是小说的uid？',
                                 cursor='xterm')
        createToolTip(
            self.whatuid,
            '小说页面网址最后的那串数字。\n比如，《边境日记》的小说页面网址是\nhttps://shequ.codemao.cn/wiki/novel/cover/52065,\n那么这本小说的uid就是52065。'
        )
        self.advanced_setting = ttk.LabelFrame(
            self.body, text='代理服务器设置（高级设置）       当前使用的代理ip及端口：未使用')

        self.soft_info = ttk.Label(self.body,
                                   style="Link.TLabel",
                                   text='软件信息',
                                   cursor='hand2')
        self.soft_info.bind("<Button-1>", self.show_softinfo)

        self.useip = tk.BooleanVar()
        self.useip_rd = ttk.Checkbutton(self.advanced_setting,
                                        text="使用代理服务器",
                                        variable=self.useip,
                                        command=self.dailip)
        createToolTip(self.useip_rd, '请在网络专家的指导下使用（如非必要请不要开启）')
        self.useip.set(False)

        self.ip_ip_tip = ttk.Label(self.advanced_setting,
                                   style="My2.TLabel",
                                   text='代理IP地址：')
        self.ip_ip_ety = ttk.Entry(self.advanced_setting)
        self.ip_port_tip = ttk.Label(self.advanced_setting,
                                     style="My2.TLabel",
                                     text='代理IP端口：')
        self.ip_port_ety = ttk.Entry(self.advanced_setting)

        self.ip_tip = ttk.Label(self.advanced_setting,
                                style="SmallTip.TLabel",
                                text='提示')
        createToolTip(
            self.ip_tip,
            '使用代理ip可能会导致爬取缓慢、爬取不完整、爬取失败，\n甚至使为你提供代理服务的代理商短暂性或永久性拒绝为你提供代理服务。\n\n请选择支持HTTPS代理的代理服务器'
        )
        self.ip_save_btn = ttk.Button(self.advanced_setting,
                                      style="My.TButton",
                                      text='保存',
                                      command=self.update_ip)
        createToolTip(self.ip_save_btn, '需要先按此按钮才能应用代理更改')

        self.ip_ip_tip['state'] = self.ip_save_btn['state'] = self.ip_ip_ety['state'] = self.ip_port_ety['state'] = \
        self.ip_port_tip['state'] = 'disabled'
        # /define
        self.display_all_w()

        self.body.mainloop()

    def display_all_w(self):
        self.uid_tip.place(x=20, y=10)
        self.uid_ety.place(x=20, y=50)
        self.intrde_txt.place(x=350, y=30)
        self.itnd_tip.place(x=360, y=10)
        self.go_btn.place(x=210, y=48)

        self.frame1.place(x=20, y=120, width=300, height=210)
        self.advanced_setting.place(x=20, y=375, width=810, height=50)
        self.cptrlist.pack()

        self.pqjdbfb.place(x=310, y=340)
        self.pb_lb.place(x=20, y=340)

        self.p1.place(x=100, y=340)
        self.type_tip.place(x=13, y=88)
        self.html_rd.place(x=120, y=85)
        self.txt_rd.place(x=200, y=85)

        self.sb.place(x=770, y=278, width=50)
        self.put.place(x=465, y=340)
        self.put_fm.place(x=350, y=340)
        self.now_novel.place(x=580, y=300)
        self.whatuid.place(x=580, y=355)

        self.fm_tip.place(x=590, y=10)
        self.soft_info.place(x=770, y=10)
        self.fm_canvas.place(x=590, y=30, width=178, height=248)
        self.unbtn.place(x=770, y=328, width=50)

        self.useip_rd.place(x=20, y=0)
        self.ip_ip_tip.place(x=150, y=2)
        self.ip_ip_ety.place(x=235, y=0)

        self.ip_port_tip.place(x=400, y=2)
        self.ip_port_ety.place(x=485, y=0)
        self.ip_tip.place(x=730, y=2)
        self.ip_save_btn.place(x=650, y=0, width=50)

    def when_close(self):
        if self.isdowning:
            answer = mBox.askyesno(
                "警告", "小说正在爬取，如果您强制关闭此窗口，可能会导致爬取的文件缺失、不完整或损坏\n确定要强制关闭吗？")
            if answer:
                self.body.quit()
                self.body.destroy()
        self.body.quit()
        self.body.destroy()

    def unselect(self):
        self.novel = None
        self.now_novel.config(text='当前要爬取的小说：{}\nuid：{}'.format('未选定', '暂无'))
        self.unbtn['state'] = 'disabled'
        self.sb['state'] = 'disabled'
        self.put['state'] = 'disabled'
        self.put_fm['state'] = 'disabled'
        self.fm_canvas.delete(tk.ALL)
        self.intrde_txt.delete(0.0, tk.END)
        self.cptrlist.delete(0.0, tk.END)

    def get_info(self):
        self.go_btn['state'] = 'disabled'
        self.useip_rd['state'] = 'disabled'
        self.uid_ety['state'] = 'disabled'
        try:
            abc = int(self.uid_ety.get())
            if abc < 1:
                raise ValueError
        except (TypeError, ValueError):
            mBox.showwarning('警告', '请输入正确的小说uid')
            self.uid_ety.delete(0, 'end')
        else:
            try:
                self.novel = novel(abc, self.dl_ip, self.dl_port)
            except Exception as e:
                self.unselect()
                mBox.showerror(
                    '错误', '网络错误，请检查代理服务器配置是否正确\n（如非必要，建议不要开启代理服务器）\n\n错误信息：{}'.
                    format(e))

            else:
                if self.novel.id is None:
                    mBox.showwarning('警告', '小说不存在！')
                    self.uid_ety.delete(0, 'end')
                    self.novel = None
                elif self.novel.isghost:
                    mBox.showwarning('警告', '小说为幽灵小说，无法爬取！')
                    self.uid_ety.delete(0, 'end')
                    self.novel = None
                else:
                    self.intrde_txt.delete(0.0, tk.END)
                    self.intrde_txt.insert(tk.END, self.novel.total_infoB)
                    self.now_novel.config(text='当前要爬取的小说：{}\nuid：{}'.format(
                        self.novel.novel_name, self.novel.id))
                    global los
                    los = ImageTk.PhotoImage(
                        Image.open(io.BytesIO(self.novel.picdata)).resize(
                            (178, 248)))  # $#
                    self.fm_canvas.create_image(0, 0, anchor='nw', image=los)
                    self.update_lis()
                    self.unbtn['state'] = 'normal'
                    self.sb['state'] = 'normal'
                    self.put['state'] = 'normal'
                    self.put_fm['state'] = 'normal'
        finally:
            self.useip_rd['state'] = 'normal'
            self.go_btn['state'] = 'normal'
            self.uid_ety['state'] = 'normal'

    def Checked(self):
        if not self.ashtml.get() and not self.astxt.get():
            mBox.showwarning('警告', '至少选择一种格式')
            self.astxt.set(True)
            self.ashtml.set(True)

    ip_states = ('disabled', 'normal')

    def dailip(self):
        tst = self.ip_states[int(self.useip.get())]
        if not self.useip.get():
            self.dl_ip = None
            self.dl_port = None
            if not (((re.match(IPCHAR,
                               self.ip_ip_ety.get().strip())
                      and re.match(r'^\d+',
                                   self.ip_port_ety.get().strip())) or
                     (self.ip_ip_ety.get().strip() ==
                      self.ip_port_ety.get().strip() == ''))):
                self.ip_ip_ety.delete(0, 'end')
                self.ip_port_ety.delete(0, 'end')
            self.advanced_setting.config(
                text='代理服务器设置（高级设置）       当前使用的代理ip及端口：未使用')
        else:
            self.update_ip(False)
        self.ip_ip_tip['state'] = self.ip_ip_ety['state'] = self.ip_port_ety['state'] = self.ip_port_tip['state'] = \
        self.ip_save_btn['state'] = tst

    def update_ip(self, frombtn=True):
        assert self.useip.get()
        ip = self.ip_ip_ety.get().strip()
        port = self.ip_port_ety.get().strip()
        if not (((re.match(IPCHAR, ip) and re.match(r'^\d+', port)) or
                 (ip == port == ''))):
            mBox.showerror('保存失败', '格式不规范的代理IP或代理端口')
            self.ip_ip_ety.delete(0, 'end')
            self.ip_port_ety.delete(0, 'end')
            if not frombtn:
                self.dl_ip = ''
                self.dl_port = ''
                self.advanced_setting.config(
                    text='代理服务器设置（高级设置）       当前使用的代理ip及端口：{}'.format(
                        '空地址空端口' if self.dl_ip.replace(' ', '') == self.
                        dl_port.replace(' ', '') == '' else '{}:{}'.
                        format(self.dl_ip, self.dl_port)))
            return
        self.dl_ip = ip
        self.dl_port = port
        if self.novel is not None:
            self.novel.dl_ip = self.dl_ip
            self.novel.dl_port = self.dl_port
        self.advanced_setting.config(
            text='代理服务器设置（高级设置）       当前使用的代理ip及端口：{}'.format(
                '空地址空端口' if self.dl_ip.replace(' ', '') == self.dl_port.
                replace(' ', '') == '' else '{}:{}'.
                format(self.dl_ip, self.dl_port)))
        if frombtn:
            mBox.showinfo('保存成功', '已保存代理设置！')

    def download(self):
        def no_name():
            self.isdowning = True
            try:
                for i in self.novel.save_each_cptr(self.ashtml.get(),
                                                   self.astxt.get()):
                    self.p1['value'] = i
                    self.pqjdbfb.config(text=str(i) + '%')
            except Exception as e:
                mBox.showerror(
                    '错误',
                    '可能是以下原因引起：\n1.您选择的{}目录下已经存在同名的小说目录。爬取不完整，\n    请自行前往该目录删除重名的文件夹和不完整的爬取结果，重新爬取。\n2.网络错误，请检查网络连接或代理服务器配置。（如果配置了的话）\n=============\n错误信息：{}'
                    .format(os.path.join(self.asdf, self.novel.dir_name), e))
                mBox.showinfo('提示', '爬取失败！')
            else:
                self.novel.save_fm()
                mBox.showinfo('提示', '爬取完毕！')
            self.go_btn['state'] = 'normal'
            self.uid_ety['state'] = 'normal'
            self.sb['state'] = 'normal'
            self.useip_rd['state'] = 'normal'
            self.html_rd['state'] = 'normal'
            self.txt_rd['state'] = 'normal'
            self.put['state'] = 'normal'
            self.put_fm['state'] = 'normal'
            self.unbtn['state'] = 'normal'
            self.pqjdbfb.config(text='0%')
            self.p1['value'] = 0
            self.isdowning = False

        try:
            while True:
                self.asdf = filedialog.askdirectory(title='选择保存目录',
                                                    initialdir=os.getcwd())
                if self.asdf == '':
                    mBox.showinfo('提示', '已取消')
                    return
                else:
                    self.novel.summon_dir(self.asdf)
                    break
        except (FileExistsError, FileNotFoundError):
            mBox.showerror(
                '错误',
                '您选择的{}目录下已经存在同名的小说目录或选择的路径不存在。爬取不完整，\n请自行前往该目录删除重名的文件夹和不完整的爬取结果，或重新选择一个存在的路径，重新爬取。'
                .format(os.path.join(self.asdf, self.novel.dir_name)))
            mBox.showinfo('提示', '爬取失败！')
        else:
            self.html_rd['state'] = 'disabled'
            self.txt_rd['state'] = 'disabled'
            self.sb['state'] = 'disabled'
            self.put['state'] = 'disabled'
            self.put_fm['state'] = 'disabled'
            self.unbtn['state'] = 'disabled'
            self.go_btn['state'] = 'disabled'
            self.uid_ety['state'] = 'disabled'
            self.useip_rd['state'] = 'disabled'
            thread = threading.Thread(target=no_name, daemon=True)
            thread.start()

    def update_lis(self):
        self.cptrlist.delete(0.0, tk.END)
        for n, i in enumerate(self.novel.cptrs):
            self.cptrlist.insert(
                tk.END,
                i['title'] + ('\n' if n != len(self.novel.cptrs) - 1 else ''))

    def outload(self):
        while True:
            save_path = filedialog.asksaveasfilename(
                defaultextension='.txt',
                title='选择导出位置',
                initialfile='{}-{}（{}）-小说信息.txt'.format(
                    self.novel.author_name, self.novel.novel_name,
                    self.novel.id),
                initialdir=os.getcwd(),
                filetypes=[('文本文档', '.txt')])
            if save_path == '':
                mBox.showinfo('提示', '已取消')
                return
            else:
                break
        try:
            with open(save_path, 'w+', encoding='utf-8') as f:
                f.write(self.novel.total_infoA)
        except Exception as e:
            mBox.showerror('错误', '导出失败，发生错误：{}'.format(e))
        else:
            mBox.showinfo('提示', '导出成功！')

    def outload_fm(self):
        while True:
            save_path = filedialog.asksaveasfilename(
                defaultextension='.jpg',
                title='选择导出位置',
                initialfile='{}-{}-uid：{}-小说封面.jpg'.format(
                    self.novel.author_name, self.novel.novel_name,
                    self.novel.id),
                initialdir=os.getcwd(),
                filetypes=[('.JPG', '.jpg')])
            if save_path == '':
                mBox.showinfo('提示', '已取消')
                return
            else:
                break
        try:
            self.novel.save_fm(filepth=save_path)
        except Exception as e:
            mBox.showerror('错误', '导出失败，发生错误：{}'.format(e))
        else:
            mBox.showinfo('提示', '导出成功！')

    def show_softinfo(self, event=None):
        mBox.showinfo(
            '软件信息',
            '版本号1.0.9(不稳定)\n2024/7/19制作完成\n作者：煤黑烧饼\n仅供学习交流使用。\nLICENSE: Apache License 2.0'
        )



if __name__ == '__main__':
    myApp = App()
