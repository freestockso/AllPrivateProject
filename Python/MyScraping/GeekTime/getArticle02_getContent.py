﻿import pdfkit, time, re, os
from bs4 import BeautifulSoup
from selenium import webdriver

# Debug 状态，网页不登陆，不滚动
inDebug = True and False

createPdf = True and False

# 滚动区域的 DIV
CLASS_SCROLL_NAME = 'ibY_sXau_0 ps'
# 抓取正文的 DIV
CLASS_SCRAP_NAME = '_1Dgl7pMn_0'

# 元素 1：文章原始标题
# 元素 2：网页地址或手工保存网页文件的绝对路径
courseList = \
[('开篇词 | 为什么要学习Kafka？', 'https://time.geekbang.org/column/article/98683'),
 ('01 |  消息引擎系统ABC', 'https://time.geekbang.org/column/article/98948'),
 ('02 | 一篇文章带你快速搞定Kafka术语', 'https://time.geekbang.org/column/article/99318'),
 ('03 | Kafka只是消息引擎系统吗？', 'https://time.geekbang.org/column/article/99797'),
 ('04 | 我应该选择哪种Kafka？', 'https://time.geekbang.org/column/article/100285'),
 ('05 | 聊聊Kafka的版本号', 'https://time.geekbang.org/column/article/100726'),
 ('06 | Kafka线上集群部署方案怎么做？', 'https://time.geekbang.org/column/article/101107'),
 ('07 | 最最最重要的集群参数配置（上）', 'https://time.geekbang.org/column/article/101171'),
 ('08 | 最最最重要的集群参数配置（下）', 'https://time.geekbang.org/column/article/101763'),
 ('09 |  生产者消息分区机制原理剖析', 'https://time.geekbang.org/column/article/102067'),
 ('10 | 生产者压缩算法面面观', 'https://time.geekbang.org/column/article/102132'),
 ('11 | 无消息丢失配置怎么实现？', 'https://time.geekbang.org/column/article/102931'),
 ('12 | 客户端都有哪些不常见但是很高级的功能？', 'https://time.geekbang.org/column/article/103397'),
 ('13 |  Java生产者是如何管理TCP连接的？', 'https://time.geekbang.org/column/article/103844'),
 ('14 | 幂等生产者和事务生产者是一回事吗？', 'https://time.geekbang.org/column/article/103974'),
 ('15 | 消费者组到底是什么？', 'https://time.geekbang.org/column/article/105112'),
 ('16 | 揭开神秘的“位移主题”面纱', 'https://time.geekbang.org/column/article/105473'),
 ('17 | 消费者组重平衡能避免吗？', 'https://time.geekbang.org/column/article/105737'),
 ('18 | Kafka中位移提交那些事儿', 'https://time.geekbang.org/column/article/106904'),
 ('19 | CommitFailedException异常怎么处理？', 'https://time.geekbang.org/column/article/107845'),
 ('20 | 多线程开发消费者实例', 'https://time.geekbang.org/column/article/108512'),
 ('21 | Java 消费者是如何管理TCP连接的?', 'https://time.geekbang.org/column/article/109121'),
 ('22 | 消费者组消费进度监控都怎么实现？', 'https://time.geekbang.org/column/article/109238'),
 ('23 | Kafka副本机制详解', 'https://time.geekbang.org/column/article/110388'),
 ('24 | 请求是怎么被处理的？', 'https://time.geekbang.org/column/article/110482'),
 ('25 | 消费者组重平衡全流程解析', 'https://time.geekbang.org/column/article/111226'),
 ('26 | 你一定不能错过的Kafka控制器', 'https://time.geekbang.org/column/article/111339'),
 ('27 | 关于高水位和Leader Epoch的讨论', 'https://time.geekbang.org/column/article/112118'),
 ('28 | 主题管理知多少?', 'https://time.geekbang.org/column/article/112202'),
 ('29 | Kafka动态配置了解下？', 'https://time.geekbang.org/column/article/113504'),
 ('30 | 怎么重设消费者组位移？', 'https://time.geekbang.org/column/article/116070'),
 ('31 | 常见工具脚本大汇总', 'https://time.geekbang.org/column/article/116111'),
 ('32 | KafkaAdminClient：Kafka的运维利器', 'https://time.geekbang.org/column/article/118319'),
 ('33 | Kafka认证机制用哪家？', 'https://time.geekbang.org/column/article/118347'),
 ('34 | 云环境下的授权该怎么做？', 'https://time.geekbang.org/column/article/120099'),
 ('35 | 跨集群备份解决方案MirrorMaker', 'https://time.geekbang.org/column/article/120991'),
 ('36 | 你应该怎么监控Kafka？', 'https://time.geekbang.org/column/article/126109'),
 ('37 | 主流的Kafka监控框架', 'https://time.geekbang.org/column/article/127192'),
 ('38 | 调优Kafka，你做到了吗？', 'https://time.geekbang.org/column/article/128184'),
 ('39 | 从0搭建基于Kafka的企业级实时日志流处理平台', 'https://time.geekbang.org/column/article/130907'),
 ('40 | Kafka Streams与其他流处理平台的差异在哪里？', 'https://time.geekbang.org/column/article/132096'),
 ('41 | Kafka Streams DSL开发实例', 'https://time.geekbang.org/column/article/132819'),
 ('42 | Kafka Streams在金融领域的应用', 'https://time.geekbang.org/column/article/134098'),
 ('加餐 | 搭建开发环境、阅读源码方法、经典学习资料大揭秘', 'https://time.geekbang.org/column/article/128613'),
 ('结束语 | 以梦为马，莫负韶华！', 'https://time.geekbang.org/column/article/135135')]




realDir = os.path.dirname(os.path.realpath(__file__))


# 用户名、密码登录网站
def Login(driver):
    """
    用户名、密码登录网站
    :param driver: 浏览器
    :return:
    """

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

    # 使用driver打开极客时间登录页面
    print("正在登录网站...")
    login_url = 'https://account.geekbang.org/login'
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


def createPdfFile(sourceHtml, pdfFileName):
    """
    :param sourceHtml: 源 html 可以是文件或 html 源码字符串
    :param pdfFileName:pdf 文件
    :return:
    """

    # 配置PDF选项 避免中文乱码
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }

    if not sourceHtml.startswith('<') and os.path.exists(sourceHtml):
        htmlFile = open(sourceHtml, 'rt', encoding='utf-8')
        html = htmlFile.read()
        htmlFile.close()
    else:
        html = sourceHtml
    html = html.replace(r'background:#000', r'background:#fff')  # 黑色背景色转成白色
    if pdfkit.from_string(html, pdfFileName, options=options):
        print("PDF 已生成。  --> %s" % (pdfFileName))


# 点击页面上的 “展开”
def ExpTag(driver):
    try:
        zhanKai = driver.find_element_by_xpath("//span[text()=\"展开\"]")
        while zhanKai is not None:
            # 页面滚动到指定元素
            driver.execute_script("arguments[0].scrollIntoView();", zhanKai)

            # 再往上翻一点点，否则可能会被登录 DIV 挡住
            driver.execute_script('window.scrollBy(0,-200)')

            zhanKai.click()

            driver.implicitly_wait(1)
            time.sleep(1)

            zhanKai = driver.find_element_by_xpath("//span[text()=\"展开\"]")
    except:
        pass

def processHtml(html, tarTitle):
    """
    处理 HTML 源码，生成文件，生成 PDF
    :param html: 原始网页的 html 源码
    :param tarTitle:生成文件的标题
    :return:
    """

    # 生成干净的 html 的模板
    modHtml = "<html>%s<body>%s</body></html>"

    bs = BeautifulSoup(html, "html.parser")

    # 专栏名称
    # columnName = bs.select_one('a[class="title"]').text.strip()
    # columnName = tarTitle
    columnName = ''

    # 保存目录
    exportPath = ("R:\\%s\\" % columnName).replace("\\\\", "\\")
    exportPathPDF = exportPath + "PDF\\"
    exportPathHTML = exportPath + "HTML\\"
    if createPdf and not os.path.exists(exportPathPDF):
        os.makedirs(exportPathPDF)
    if not os.path.exists(exportPathHTML):
        os.makedirs(exportPathHTML)

    # 获取 m3u8 文件地址
    m3u8 = bs.find("audio")
    if m3u8 is not None:
        ffmpeg = 'ffmpeg -i %s -vcodec copy -acodec copy "%s.aac"\n' % (m3u8["src"], tarTitle)

        # 写 ffmpeg 下载列表
        ffmpegListFile = open(exportPath + "ffmpegDownList.txt", 'a', encoding='gb2312')
        ffmpegListFile.write(ffmpeg)
        ffmpegListFile.close()

    # 获取干净的 html 并保存
    [s.extract() for s in bs.find_all("script")]  # 去干净 JS
    headHtml = bs.find("head")
    headHtml = repr(headHtml).replace('="//static001.', '="https://static001.')  # 替换标签图标路径
    bodyDivHtml = bs.find("div", {"class": CLASS_SCRAP_NAME})
    targetHtml = modHtml % (headHtml, bodyDivHtml)
    targetHtml = targetHtml.replace('CFSR', '')  # 去掉私人信息
    htmlFile = open(exportPathHTML + tarTitle + '.html', 'w', encoding='utf-8')
    htmlFile.write(targetHtml)
    htmlFile.close()
    print("Html 抓取完成。  --> %s.html" % (tarTitle))

    # 用 html 生成 PDF 文件
    if createPdf:
        createPdfFile(targetHtml, exportPathPDF + tarTitle + '.pdf')


# 滚到最底端，获取完整的网页内容
def scrollDrive2Bottom(driver):
    # pageHeight_orig = driver.execute_script('return document.body.scrollHeight')
    # while True:
    #     driver.execute_script('window.scrollBy(0,50000)')
    #     time.sleep(3)
    #     pageHeight_new = driver.execute_script('return document.body.scrollHeight')
    #
    #     if pageHeight_new == pageHeight_orig:
    #         break
    #     else:
    #         pageHeight_orig = pageHeight_new

    divHeightOrg = driver.execute_script(
        'return document.getElementsByClassName(\'' + CLASS_SCROLL_NAME + '\')[0].scrollTop')
    while True:
        driver.execute_script('document.getElementsByClassName(\'' + CLASS_SCROLL_NAME + '\')[0].scrollTop += 5000')
        time.sleep(3)
        divHeightNew = driver.execute_script(
            'return document.getElementsByClassName(\'' + CLASS_SCROLL_NAME + '\')[0].scrollTop')

        if divHeightNew == divHeightOrg:
            break
        else:
            divHeightOrg = divHeightNew

    # 点击页面上的 “展开”
    ExpTag(driver)


def main():
    # 抓取成功的数量
    catchCount = 0

    # 抓取失败的列表
    errList = []

    t, f = courseList[0]
    isFile = os.path.exists(f)

    print("开始爬取专栏文章...")
    # 记录爬取文章的开始时间
    start = time.time()

    if isFile:
        for doc in courseList:
            title, fileFullName = doc
            tarTitle = re.sub('[\/:：*?"<>|]', '', title.strip()).replace('  ', ' ')

            try:
                file = open(fileFullName, 'rt', encoding='UTF-8')
                html = file.read()
                file.close()

                # 处理 HTML 源码，生成文件，生成 PDF
                processHtml(html, tarTitle)
            except:
                errList.append(title)

            catchCount += 1
            print("\n\n")
    else:

        # 定义chromedriver路径
        driver_path = realDir + r'\..\..\virtualEnv\chromedriver_2.43\chromedriver.exe'

        # 获取chrome浏览器驱动
        driver = webdriver.Chrome()  # executable_path=driver_path

        if not inDebug:
            Login(driver)

        # 正式开始抓取
        for doc in courseList:
            title, url = doc
            tarTitle = re.sub('[\/:：*?"<>|]', '', title.strip()).replace('  ', ' ')

            try:
                print("正在抓取文章：" + tarTitle)
                driver.get(url)
                driver.implicitly_wait(5)
                time.sleep(5)

                # 滚到最底端，获取完整的网页内容
                if not inDebug or inDebug:  # 有时候不滚到最底下会抓出来空白的
                    scrollDrive2Bottom(driver)

                # 处理 HTML 源码，生成文件，生成 PDF
                processHtml(driver.page_source, tarTitle)
            except:
                errList.append(title)

            # 爬一篇文章后休息几秒钟
            catchCount += 1
            time.sleep(5)
            print("\n\n")

    # 记录爬取文章的结束时间
    end = time.time()

    print("ffmpeg 下载列表  --> ffmpegDownList.txt")
    print("所有文章爬取完毕！共 %d 篇，耗时 %d 秒" % (catchCount, int(end - start)))

    if len(errList) > 0:
        print("失败的抓取：")
        for name in errList: print(name)


if __name__ == '__main__':
    main()
