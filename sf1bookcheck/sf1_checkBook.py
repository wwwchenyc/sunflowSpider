# -*- coding: utf-8 -*-
import requests 
import json
import re
import csv
import time

import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

def GetAllClassifyBook():
	result = requests.get("http://estudy.intretech.com:9090/estudy/book/GetAllClassifyBook")
	# print(result.text)
	return result.text
	pass
def getClassifyBook(cateId,page):
	#创建,完善字典
	param  = {"cateId":1 ,"page":1}
	param['cateId'] = cateId
	param['page'] = page
	#拼接json
	paramstr = json.dumps(param)
	#组建参数，发出post请求
	params = {'paramStr':paramstr} 
	result = requests.post('http://estudy.intretech.com:9090/estudy/book/getClassifyBook', data=params)
	# print(result.text)
	return result.text
def getBookDetail(bookId):	
	#创建,完善字典
	param  = {"bookId":"1"}
	param['bookId'] = bookId
	#拼接json
	paramstr = json.dumps(param)
	#组建参数，发出post请求
	params = {'paramStr':paramstr} 
	result = requests.post('http://estudy.intretech.com:9090/estudy/book/getBookDetail', data=params)
	# print(result.text)
	return result.text
	pass

global oknum
oknum = 0

def checkurl(url):
	global unUseUrl
	kv={'user-agent':'Mozilla/5.0'}
	result = requests.get(url,headers=kv)
	response = re.findall(r'对不起，您要访问的页面暂时没有找到',result.text)
	if len(response) > 0:
		print("%d:::::对不起，您要访问的页面暂时没有找到"%unUseUrl)
		unUseUrl=unUseUrl+1
		return False
	else:
		global oknum
		print("url ok．unUseUrl：%d  "%oknum)
		oknum+=1
		return True
	pass

def saveInfoToCsv(List):
    try:
        f=open('./unUseBook'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.csv','a+')#,newline = '')
        csvwriter = csv.writer(f)
        headers = ['bookName','bookId','bookCover','author','publisher','authorDetail','content','purchaseUrl','recommendation']
        csvwriter.writerow(headers)
        for row in List:
            # print(row)
            csvwriter.writerow(row)
        f.close()
    except Exception as e:
        print(e)
        print("save csv file fail!!!!!!!!!!")
    pass

unUseUrl=0
unUseBookList=[]
def main():
	global unUseBookList
	#获取分类数量
	data = json.loads(GetAllClassifyBook())
	classData = data.get("data")
	# print("classnum:%d"%len(classData))
	for x in range(len(classData)):
		#获取不同分类绘本的ｉｄ和书本数量 并遍历
		cateId = classData[x].get("cateId")
		bookCount = classData[x].get("bookCount")
		print("------------------------------------cateId:%d-----------------------------------------"%cateId)
		# print("bookCount:%d"%bookCount)
		i=1
		while bookCount > 0:
			#遍历同类别的书籍
			reponse = json.loads(getClassifyBook(cateId,i))
			i=i+1
			booklist = reponse.get("data")
			if booklist != None:
				bookCount = bookCount-len(booklist)
				for y in range(len(booklist)):
					#获取书籍详细信息
					bookId = booklist[y].get("bookId")
					# print("bookName:%s,bookId:%s"%(bookName,bookId))
					response = json.loads(getBookDetail(bookId))
					bookInfo = response.get("data")
					bookName = bookInfo.get("bookName")
					bookCover = bookInfo.get("bookCover")
					author = bookInfo.get("author")
					publisher = bookInfo.get("publisher")
					authorDetail = bookInfo.get("authorDetail")
					content = bookInfo.get("content")
					purchaseUrl = bookInfo.get("purchaseUrl")
					recommendation = bookInfo.get("recommendation")
					# print("%s  url:%s"%(bookName,purchaseUrl))
					if checkurl(purchaseUrl) is False:
						print(":::::对不起，您要访问的页面暂时没有找到")
						unUseBookList.append([bookName,bookId,bookCover,author,publisher,authorDetail,content,purchaseUrl,recommendation])
						print(unUseBookList)
						pass
					pass
				# print(bookCount)
			else:
				print("booklist is nome")
			pass
		pass
	#判断绘本链接是否有效
	#
	#
	pass
	# print("000000000000000000000000000000000000000000000000000000000000")
	print(unUseBookList)
	saveInfoToCsv(unUseBookList)
pass



if __name__ == '__main__':
	main()
	

# params = json.loads(result.text)

# data = params.get('data')
# if data != None:
# 	for i in range(len(data)):
# 		bookName = data[i].get('bookName')
# 		bookId = data[i].get('bookId')
# 		bookCover = data[i].get('bookCover')
# 		print("------------------%d------------------------"%i)
# 		print("bookName:%s"%bookName)
# 		print("bookId:%s"%bookId)
# 		# print("bookCover:%s"%bookCover)

# else:
# 	print("data is null")