import pdfkit, time, re, os
from bs4 import BeautifulSoup
from selenium import webdriver

'''
# 获取 m3u8 文件地址
ffmpegList=[]
m3u8 = driver.find_element_by_tag_name('audio').get_attribute('src')
ffmpeg = 'ffmpeg -i %s -vcodec copy -acodec copy "R:\%s.mp4"' % (m3u8, raw_title)
ffmpegList.append(ffmpeg)

# 滚到最底端
pageHeight_orig = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollBy(0,10000)')
    driver.implicitly_wait(2)
    time.sleep(3)
    pageHeight_new = driver.execute_script('return document.body.scrollHeight')

    if pageHeight_new == pageHeight_orig:
        break
    else:
        pageHeight_orig = pageHeight_new

# Write to html
modHtml = "<html>%s<body>%s</body></html>"
headHtml = bs.find("head")
bodyDivHtml = bs.find("div", {"id": "app"})
targetHtml = modHtml % (headHtml, bodyDivHtml)
    
fileObj = open('R:\\' + raw_title + '.html', 'w', encoding='utf-8')
fileObj.write(targetHtml)
fileObj.close()
'''

courseList = \
 \
    [
     ('10 通道的基本操作', 'https://time.geekbang.org/column/article/14660'),
     ('11 通道的高级玩法', 'https://time.geekbang.org/column/article/14664'),
     ('12 使用函数的正确姿势', 'https://time.geekbang.org/column/article/14671'),
     ('13 结构体及其方法的使用法门', 'https://time.geekbang.org/column/article/18035'),
     ('14 接口类型的合理运用', 'https://time.geekbang.org/column/article/18037'),
     ('15 关于指针的有限操作', 'https://time.geekbang.org/column/article/18042'),
     ('16 go语句及其执行规则（上）', 'https://time.geekbang.org/column/article/39841'),
     ('17 go语句及其执行规则（下）', 'https://time.geekbang.org/column/article/39844'),
     ('18 if语句、for语句和switch语句', 'https://time.geekbang.org/column/article/39858'),
     ('19 错误处理（上）', 'https://time.geekbang.org/column/article/40311'),
     ('20 错误处理 （下）', 'https://time.geekbang.org/column/article/40333'),
     ('21 panic函数、recover函数以及defer语句 （上）', 'https://time.geekbang.org/column/article/40359'),
     ('22 panic函数、recover函数以及defer语句（下）', 'https://time.geekbang.org/column/article/40889'),
     ('23 测试的基本规则和流程 （上）', 'https://time.geekbang.org/column/article/41036'),
     ('24 测试的基本规则和流程（下）', 'https://time.geekbang.org/column/article/41189'),
     ('25 更多的测试手法', 'https://time.geekbang.org/column/article/41255'),
     ('26 sync.Mutex与sync.RWMutex', 'https://time.geekbang.org/column/article/41350'),
     ('27 条件变量sync.Cond （上）', 'https://time.geekbang.org/column/article/41588'),
     ('28 条件变量sync.Cond （下）', 'https://time.geekbang.org/column/article/41717'),
     ('29 原子操作（上）', 'https://time.geekbang.org/column/article/41908'),
     ('30 原子操作（下）', 'https://time.geekbang.org/column/article/41929'),
     ('31 sync.WaitGroup和sync.Once', 'https://time.geekbang.org/column/article/42156'),
     ('32 context.Context类型', 'https://time.geekbang.org/column/article/42158'),
     ('33 临时对象池sync.Pool', 'https://time.geekbang.org/column/article/42160'),
     ('34 并发安全字典sync.Map （上）', 'https://time.geekbang.org/column/article/42798'),
     ('35 并发安全字典sync.Map (下)', 'https://time.geekbang.org/column/article/42800'),
     ('36 unicode与字符编码', 'https://time.geekbang.org/column/article/64407'),
     ('37 strings包与字符串操作', 'https://time.geekbang.org/column/article/64877'),
     ('38 bytes包与字节串操作（上）', 'https://time.geekbang.org/column/article/64879'),
     ('39 bytes包与字节串操作（下）', 'https://time.geekbang.org/column/article/64881'),
     ('40 io包中的接口和工具 （上）', 'https://time.geekbang.org/column/article/67474'),
     ('41 io包中的接口和工具 （下）', 'https://time.geekbang.org/column/article/67477'),
     ('42 bufio包中的数据类型 （上）', 'https://time.geekbang.org/column/article/67485'),
     ('43 bufio包中的数据类型（下）', 'https://time.geekbang.org/column/article/68776'),
     ('44 使用os包中的API （上）', 'https://time.geekbang.org/column/article/68779'),
     ('45 使用os包中的API （下）', 'https://time.geekbang.org/column/article/68782'),
     ('46 访问网络服务', 'https://time.geekbang.org/column/article/69742'),
     ('47 基于HTTP协议的网络服务', 'https://time.geekbang.org/column/article/69808'),
     ('48 程序性能分析基础（上）', 'https://time.geekbang.org/column/article/69812'),
     ('49 程序性能分析基础（下）', 'https://time.geekbang.org/column/article/70805'),
     ('50 学习专栏的正确姿势', 'https://time.geekbang.org/column/article/71043'),
     ('尾声 愿你披荆斩棘，所向无敌', 'https://time.geekbang.org/column/article/71485'),
     ('新年彩蛋 完整版思考题答案', 'https://time.geekbang.org/column/article/80362')]


def main():
    # 抓取成功的数量
    catchCount = 0

    # 生成干净的 html 的模板
    modHtml = "<html>%s<body>%s</body></html>"

    # 配置PDF选项 避免中文乱码
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }

    realDir = os.path.dirname(os.path.realpath(__file__))

    # 用户名密码
    userId = ""
    password = ""
    pwdFilePath = realDir + '\\password.txt'
    if os.path.exists(pwdFilePath):
        pFile = open(pwdFilePath)
        userId = pFile.readline().strip()
        password = pFile.readline().strip()
        pFile.close()
    if userId == "": userId = input("UserId:")
    if password == "": password = input("Password:")

    # 定义chromedriver路径
    driver_path = realDir + r'\..\..\virtualEnv\chromedriver_2.43\chromedriver.exe'
    # 获取chrome浏览器驱动
    driver = webdriver.Chrome(executable_path=driver_path)

    ''''''
    # 使用driver打开极客时间登录页面
    print("正在登录网站...")
    login_url = 'https://account.geekbang.org/signin'
    driver.get(login_url)

    # 输入手机号
    driver.find_element_by_class_name("nw-input").send_keys(userId)
    # 输入密码
    driver.find_element_by_class_name("input").send_keys(password)
    # 点击登录按钮
    driver.find_element_by_class_name("mybtn").click()
    # 为了使ajax加载完成 此处使用隐式等待让程序等待5秒钟
    driver.implicitly_wait(5)
    time.sleep(3)
    print("已登录。")

    print("开始爬取专栏文章...")
    # 记录爬取文章的开始时间
    start = time.time()

    # 正式开始抓取
    for doc in courseList:
        title, url = doc
        tarTitle = re.sub('[\/:：*?"<>|]', '', title.strip()).replace('  ', ' ')

        print("正在抓取文章：" + tarTitle)
        driver.get(url)

        # 滚到最底端，获取完整的网页内容
        pageHeight_orig = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollBy(0,50000)')
            time.sleep(3)
            pageHeight_new = driver.execute_script('return document.body.scrollHeight')

            if pageHeight_new == pageHeight_orig:
                break
            else:
                pageHeight_orig = pageHeight_new

        # 获取到网页完整内容
        bs = BeautifulSoup(driver.page_source, "html.parser")

        # 专栏名称
        # columnName = bs.select_one('a[class="title"]').text.strip()
        # columnName = tarTitle
        columnName = ''

        # 保存目录
        exportPath = "R:\\%s\\" % columnName
        exportPathPDF = exportPath + "PDF\\"
        exportPathHTML = exportPath + "HTML\\"
        if not os.path.exists(exportPathPDF):
            os.makedirs(exportPathPDF)
        if not os.path.exists(exportPathHTML):
            os.makedirs(exportPathHTML)

        # 获取 m3u8 文件地址
        m3u8 = bs.find("audio")
        if m3u8 is not None:
            ffmpeg = 'ffmpeg -i %s -vcodec copy -acodec copy "%s.mp4"\n' % (m3u8["src"], tarTitle)

            # 写 ffmpeg 下载列表
            ffmpegListFile = open(exportPath + "ffmpegDownList.txt", 'a', encoding='gb2312')
            ffmpegListFile.write(ffmpeg)
            ffmpegListFile.close()

        # 获取干净的 html 并保存
        [s.extract() for s in bs.find_all("script")]  # 去干净 JS
        headHtml = bs.find("head")
        bodyDivHtml = bs.find("div", {"id": "app"})
        targetHtml = modHtml % (headHtml, bodyDivHtml)
        htmlFile = open(exportPathHTML + tarTitle + '.html', 'w', encoding='utf-8')
        htmlFile.write(targetHtml)
        htmlFile.close()
        print("Html 抓取完成。  --> %s.html" % (tarTitle))

        ''''''
        # 用 html 生成 PDF 文件
        print("正在生成 PDF...")
        if pdfkit.from_string(targetHtml.replace(r'background:#000',r'background:#fff'), exportPathPDF + tarTitle + '.pdf', options=options):
            print("PDF 已生成。  --> %s.pdf" % (tarTitle))


        # 爬一篇文章后休息几秒钟
        catchCount += 1
        time.sleep(5)
        print("\n\n")

    # 记录爬取文章的结束时间
    end = time.time()

    print("ffmpeg 下载列表  --> ffmpegDownList.txt")
    print("所有文章爬取完毕！共 %d 篇，耗时 %d 秒" % (catchCount, int(end - start)))


if __name__ == '__main__':
    main()
