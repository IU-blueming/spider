# spider
一些简单的爬虫案列

### 什么是scrapy

- 文档地址：http://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/overview.html

- Scrapy 使用了Twisted['twɪstɪd]异步网络框架，可以加快我们的下载速度。

- **Scrapy是一个为了爬取网站数据，提取结构性数据，高性能的持久化存储而编写的应用框架**，我们只需要实现少量的代码，就能够快速的抓取



## 一、基于Scrapy的全站数据爬取

**何为全站数据爬取** : 就是将网站中某板块全部页码对应的数据进行爬取

**需求：**全站爬取校花网中的照片的名称

**分析：**

- 网址 http://www.521609.com/meinvxiaohua/
- 使用scrapy框架 编写爬虫程序

- 对全部页码的校花图片的名称进行爬取实现方案

## 二、基于ImagesPipeline实现图片数据爬取

### 1.知识点

**基于Scrapy爬字符串与图片区别**

- 字符串：只需要基于xpath进行解析且提交管道进行持久化存储
- 图片：xpath解析出图片src的属性值。单独的对图片地址发起请求获取图片二进制类型的数据

**ImagesPipeline管道介绍**

- ImagesPipeline是Scrapy中的一个pipe管道组件的一个插件模块，封装了对图片爬取的一些处理，是Scrapy给出的图片处理方案

- 只需要将img的src的属性值进行解析，提交到管道，管道就会对图片的src进行请求发送获取图片的二进制类型的数据，且还会进行持久化存储。

### 2.案例

 **需求：**爬取站长素材中的高清图片(http://sc.chinaz.com/tupian/)

**流程分析**

- 数据解析（图片的地址）
- 将存储图片地址的item提交到制定的管道类
- 在管道文件中编写一个基于ImagesPipeLine的一个管道类
    - get_media_request():  给定一个图片的url请求
    - file_path: 给定一个存储的文件名
    - item_completed ： 这个item 处理完后，接下来干什么
- 在配置文件settings中：
    - 指定图片存储的根目录：IMAGES_STORE = 'xxx'
    - 指定开启的管道：自定制的管道类
    
## 三、爬取网易新闻中五大板块

**需求：**爬取网易新闻中五大板块(国内，国际，军事，航空，无人机)的新闻数据（标题和内容）`https://news.163.com/`

**需求分析：**

- 1.通过网易新闻的首页解析出五大板块对应的详情页的url
- 2.每一个板块对应的新闻标题都是动态加载出来的（动态加载）
- 3.通过解析出每一条新闻详情页的url获取详情页的页面源码，解析出新闻内容

## 四、使用CrawlSpider采集四川问政网站中的信息

**需求：**采集四川问政网站中提问 (标题、日期，内容)等信息   

**需求分析：**

- 爬取的数据没有在同一张页面中
- 使用CrawlSpider 爬取数据
  - 可以使用链接提取器提取所有的页码链接
  - 让链接提取器提取所有的新闻详情页的链接
-命令： scrapy genspider -t crawl <爬虫名字> <允许爬取的域名>
#### 使用管道持久化数据到mysql中

## 五、增量式爬虫

**概念：**监测网站数据更新的情况，只会爬取网站最新更新出来的数据。

**需求：**增量式爬取`4567电影网`每部电影名称及描述信息

**思路分析：**

- 指定一个起始url ：http://www.4567kan.com/frim/index1.html

- 基于CrawlSpider获取其他页码链接

- 基于Rule将其他页码链接进行请求

- 从每一个页码对应的页面源码中解析出每一个电影详情页的URL
#### 使用管道持久化数据到mongdb中

## 六. 分布式爬虫实现流程

#### 1.创建一个scrapy工程

   scrapy startproject fbsproject

#### 2.创建一个基于CrawlSpider的爬虫文件

  scrapy genspider -t crawl fbs www.xxx.com

 对settings.py设置 robots设置， ua设置 

####  3.修改当前的爬虫文件：

   - 导包：from scrapy_redis.spiders import RedisCrawlSpider
- 将start_urls和allowed_domains进行注释
- 添加一个新属性：redis_key = 'movie' 可以被共享的调度器队列的名称
- 编写数据解析相关的操作
- 将当前爬虫类的父类修改成RedisCrawlSpider

#### 4.修改配置文件settings

- **指定使用可以被共享的管道：**
          ITEM_PIPELINES = {
              'scrapy_redis.pipelines.RedisPipeline': 400
          }

- **指定调度器：**
  
  - 增加了一个去重容器类的配置, 作用使用Redis的set集合来存储请求的指纹数据, 从而实现请求去重的持久化
       DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
       
  - 使用scrapy-redis组件自己的调度器
       SCHEDULER = "scrapy_redis.scheduler.Scheduler"
       
  - 配置调度器是否要持久化, 也就是当爬虫结束了, 要不要清空Redis中请求队列和去重指纹的set。如果是True, 就表示要持久化存储, 就不清空数据, 否则清空数据
   SCHEDULER_PERSIST = True
  
  - 指定redis数据库
  
      REDIS_HOST = '127.0.0.1' #redis远程服务器的ip
      REDIS_PORT = 6379

#### 5.redis相关操作配置：

- 配置redis的配置文件：

  - linux或者mac：redis.conf
  - windows:    redis.windows.conf
  - 打开配置文件修改：
    - 将bind 127.0.0.1进行注释(在windows环境测试时 ，先不要注释)
    - 关闭保护模式：protected-mode yes改为no

- 结合着配置文件开启redis服务器、客户端

#### 6.执行工程

- scrapy runspider xxx.py

#### 7.向调度器的队列中投入一个起始的url

- 调度器的队列在redis的客户端中

   - lpush 队列key名  http://www.4567kan.com/frim/index1.html
   - lpush movie  http://www.4567kan.com/frim/index1.html

#### 8.爬取的数据存储在redis的proName:item这个数据结构中

在redis 客户端 操作如下命令：

- keys *
- lrange  key  start end
- llen  key
