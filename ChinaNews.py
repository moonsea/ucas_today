#coding=UTF-8
import re,urllib,socket,os,datetime,sys,time
from sgmllib import SGMLParser
import sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

#下载配置
#defaultSiteList = ["ZXW","163","RMW","SINA","IFENG"] #新闻源站点设置
defaultSiteList = ["ZXW"] #新闻源站点设置
defaultMaxNews = 100
argD = os.getcwd()+os.path.sep+'dataNews'#default目录
newsListFilePath = os.getcwd()+os.path.sep

#默认开始结束时间
defaultStartTime = "2015-12-01"
defaultEndTime = "2015-12-31"

#默认Url连接超时时间
defaultSockTimeLimit = 20

dirForDiv = {'ZXW':['class','left_zw']}
#定义从滚动新闻页面提取出新闻Url的正则表达式
# dirRegex = {'ZXW':r'<div id="nav"><a href=[^<>]*>[^<>]*</a> → <a href=[^<>]*>[^<>]*</a> → <a href=[^<>]*>[^<>]*</a>'}
dirRegex = {'ZXW':r'<div class=\"dd_bt\"><a href=[^<>]*>[^<>]*</a></div><div class=\"dd_time\">[\d]{1,2}-[\d]{1,2} [\d]{2}:[\d]{2}</div>'}

class GetNewsParser(SGMLParser):
	"""
	继承SGMLParser
	提取出新闻的正文内容
	"""
	def __init__(self,site="163"):
		SGMLParser.__init__(self)
		self.site = site
	def reset(self):
		self.newsText = []
		self.flag = False
		self.getdata = False
		self.verbatim = 0
		SGMLParser.reset(self)
		
	def start_div(self,attrs):
		if self.flag == True:
				self.verbatim += 1
				return

		for k,v in attrs:
				if k == dirForDiv[self.site][0] and v == dirForDiv[self.site][1]:
						self.flag = True
						return
	
	def end_div(self):
		if self.verbatim == 0:
				self.flag = False
		if self.flag == True:
				self.verbatim -= 1
	
	def start_p(self,attrs):
		if self.flag == False:
				return
		self.getdata = True
	def end_p(self):
		if self.getdata:
				self.getdata = False
	def start_script(self,attrs):
		if self.getdata and self.site == "ZXW":
			self.getdata = False
	def handle_data(self,text):
		if self.getdata:
				self.newsText.append(text)

class GetChinaNews():
	def __init__(self,str_start_time=defaultStartTime,str_end_time=defaultEndTime,dirName=os.getcwd(),siteList=defaultSiteList,timeLimit=defaultSockTimeLimit):
	#s:str_start_time,e:str_end_time,d:dirName,l:sitelist,t:timeLimit
		self.date_range = self.dateRange(str_start_time,str_end_time)
		self.dir_name = dirName
		self.root_dir_name = dirName
		self.siteList = siteList
		socket.setdefaulttimeout(timeLimit)
		self.strYear = "2015"
		self.strMonth = "12"
		self.strDay = "01"
		self.Url = "This is the roll news page Url."
		self.tag  = 0
		self.newsList = []
		
	
	#set the date range that get news
	def dateRange(self,str_start_time,str_end_time):
		"""
		set the date range
		"""
		tmp = str_start_time.split('-')
		tmp1 = str_end_time.split('-')
		start_time = datetime.datetime(int(tmp[0]),int(tmp[1]),int(tmp[2]))
		end_time = datetime.datetime(int(tmp1[0]),int(tmp1[1]),int(tmp1[2]))
		for n in range(int((end_time-start_time).days)):
			yield start_time + datetime.timedelta(n)

	def getNewsProperties(self,site,str):
		"""
		return the list [newsTitle,newsUrl,newsTime]
		"""
		if site == "ZXW" or site == "RMW" or site == "IFENG":
			delimiter = '>'
		else:
			delimiter = '"'
		iList = str.split(delimiter)
		
		if site == "ZXW":
			return [iList[2][:-3],iList[1][9:-1],self.strYear+'-'+self.strMonth+'-'+self.strDay+' '+iList[5].split(' ')[1][:-5]+":00"]
		
	def getNewsFromRollPage(self,site):
		htmlSource = ""
		try:
			sock = urllib.urlopen(self.Url)
			htmlSource = sock.read()
			# print htmlSource
			sock.close()
		except:
			print "Something wrong when openning NewsPage:"+self.Url
				
		m = re.findall(dirRegex[site],htmlSource,re.M)
		newsUrl = "NONE"
		for i in m:
			try:
				#从网页上获取新闻属性
				newsTitle,newsUrl,newsTime = self.getNewsProperties(site,i)
				#special for ZXW
				if site == "ZXW" and newsUrl[:4] != "http":
					newsUrl = "http://www.chinanews.com" + newsUrl

				sock = urllib.urlopen(newsUrl)
				htmlSource = sock.read()
				sock.close()
					
				#use Parser to get text content of news,stored in strText
				getcontent = GetNewsParser(site)
				getcontent.feed(htmlSource)
				strText = ""
				for k in getcontent.newsText:
					strText += k
				getcontent.close()
				fileName = site+"-"+str(self.tag)
				self.tag = self.tag + 1

				# Write Sqlites3
				con = sqlite3.connect("./db/development.sqlite3")
				cu = con.cursor()
				cu_url = newsUrl.strip().split("/")
				cu_info = cu_url[3].strip()
				# print cu_info
				con.execute("insert into articles(title,text,author_id,info,created_at,updated_at) values('"+newsTitle.strip().decode('gbk').encode('utf-8')+"','"+strText.strip().decode('gbk').encode('utf-8')+"',1,'"+cu_info.decode('gbk').encode('utf-8')+"','"+newsTime.strip()+"','"+newsTime.strip()+"')")
				print cu_info
				con.commit()
				con.close()


				#store in .txt files
				txtSource = newsTitle.strip()+"\n"+newsUrl.strip()+"\n"+newsTime.strip()+"\n"+strText.strip()
				#将IFENG的默认编码设置为gb2312（与大部分一致）
				with open(self.dir_name+fileName+'.txt','w+') as f:
					f.write(txtSource)
				
				#将获取的新闻保存以便排序，新闻属性包括（标题、文件路径、发表时间、来源网站）
				stime = time.mktime(time.strptime(newsTime, '%Y-%m-%d %H:%M:%S'))
				self.newsList.append((newsTitle,self.dir_name+fileName+'.txt',stime,site))
			except KeyboardInterrupt:
				print "Stopped By User."
				sys.exit(0)
			except:
				print "SomethinWrong when getting "+site+" news:"+newsUrl
		return True


	def getNewsFromSite(self,site):	
		
		self.tag = 0
		#the rollNewsUrl of every site
		if site == "ZXW":
			self.Url = "http://www.chinanews.com/scroll-news/" + self.strYear + "/" + self.strMonth + self.strDay + "/news.shtml"
			self.getNewsFromRollPage(site)

		print "Get "+ str(self.tag) + " " + site + " news successfully." 
		
	def getChinaNews(self):
		try:
			for tt in self.date_range:
				print "Get News From Date:"+str(tt)
				self.strYear = str(tt.year)
				if tt.month < 10:
					self.strMonth = "0" + str(tt.month)
				else:
					self.strMonth = str(tt.month)
				if tt.day < 10:
					self.strDay = "0" + str(tt.day)
				else:
					self.strDay = str(tt.day)
				#create folder for the date tt
				self.dir_name = self.root_dir_name + "/"+self.strYear+self.strMonth+self.strDay+"/"
				isExists = os.path.exists(self.dir_name)
				if not isExists:
					os.mkdir(self.dir_name)
				for i in self.siteList:
					if i in defaultSiteList:
						self.getNewsFromSite(i)
			#获取的新闻按照时间排序并输出到newsList.txt文件中
			self.newsList.sort(key=lambda d:d[2])
			with open(newsListFilePath+'newslist.txt','wa') as newslistFile:
				newslistFile.write('===========NEWS_LIST'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'============\n')
				for i in self.newsList:
					newslistFile.write(i[3]+"###"+i[0]+"###"+i[1]+"###"+str(i[2])+"\n")
		except KeyboardInterrupt:
			print "Stopped By User."
			sys.exit(0)
		except:
			print "Somethin wrong when getting chinanews."
#"2013-11-01","2013-12-01",dirName='D:/testnews',timeLimit=20
#s:str_start_time,e:str_end_time,d:dirName,t:timeLimit
argST = defaultStartTime
argED = defaultEndTime

argT = defaultSockTimeLimit
args = sys.argv
if not os.path.exists(argD):
	os.mkdir(argD)

if len(args) == 1:
	#default spider today's news
	argST = time.strftime('%Y-%m-%d')
	argED = time.strftime('%Y-%m-%d',time.localtime(time.time()+86400))
				
G = GetChinaNews(str_start_time=argST,str_end_time=argED,dirName=argD,siteList=defaultSiteList,timeLimit=argT)
G.getChinaNews()