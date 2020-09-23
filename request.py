import requests
import json
import re


def writeFile(filename,content):
	f = open(filename,'wb')
	f.write(content)
	f.close()
def getpdflink(companycode):
	url2 = 'http://query.sse.com.cn/security/stock/queryCompanyBulletin.do'
	header2 = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Connection': 'keep-alive',
	'Cookie': 'yfx_c_g_u_id_10000042=_ck20092114143215794563727502126; yfx_mr_f_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000042=; JSESSIONID=46B655B17B571AD4529A0DA116C50771; yfx_f_l_v_t_10000042=f_t_1600668872571__r_t_1600737286966__v_t_1600751175161__r_c_1; VISITED_MENU=%5B%228535%22%2C%229055%22%2C%228536%22%2C%228307%22%2C%229062%22%2C%229729%22%5D; VISITED_STOCK_CODE=%5B%22600333%22%2C%22600257%22%2C%22600965%22%2C%22600812%22%2C%22600815%22%2C%22600814%22%5D; VISITED_COMPANY_CODE=%5B%22600333%22%2C%22600257%22%2C%22600965%22%2C%22600812%22%2C%22600815%22%2C%22600814%22%5D; seecookie=600815%20%u5E74%u62A5%2C%5B600333%5D%3A%u957F%u6625%u71C3%u6C14%2C600815%2C%u5E74%u62A5600815%2C%5B600812%5D%3A%u534E%u5317%u5236%u836F%2C%5B600815%5D%3A*ST%u53A6%u5DE5%2C%5B600814%5D%3A%u676D%u5DDE%u89E3%u767E',
	'Host': 'query.sse.com.cn',
	'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/announcement/index.shtml?productId='+companycode,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
	}
	data2 = {
		'jsonCallBack':'jsonpCallback38714',
		'isPagination':'true',
		'productId':companycode,
		'keyWord':'',
		'securityType':'0101',
		'reportType2':'DQBG',
		'reportType':'YEARLY',
		'beginDate':'2017-09-23',
		'endDate':'2020-09-22',
		'pageHelp.pageSize':'25',
		'pageHelp.pageCount':'50',
		'pageHelp.pageNo':'1',
		'pageHelp.beginPage':'1',
		'pageHelp.cacheSize':'1',
		'pageHelp.endPage':'5',
		'_':'1600738394577'
	}
	r2 = requests.post(url2,headers=header2,data=data2)
	r = re.findall(r'[(](.*?)[)]', r2.text)[0]
	d = json.loads(r)['result']
	res = {}
	for item in d:
		res['./download/'+companycode +'---'+ item['TITLE'].replace('*','')+'.pdf'] = "http://static.sse.com.cn" + item['URL'] 
		# filename = './download/'+companycode +'---'+ item['TITLE']
		# content = requests.get("http://static.sse.com.cn" + item['URL'] )
		# writeFile(filename,content)
		# print(filename,'->',"http://static.sse.com.cn" + item['URL'])
	return res

def getcompanycode():
	d = []
	i = 1
	with open("company.txt", "r", encoding='UTF-8') as f:
		lines  = f.readlines()
		for line in lines:
			if i==18:
				line = json.loads(line[19:-1])
			else:
				line = json.loads(line[19:-2])
			d += line['result']
			i+=1
	return d
codes = getcompanycode()

for i in range(len(codes)):
	companycode = codes[i]['companycode']
	print("正在下载第"+str(i+1)+"个公司("+codes[i]['fullname']+")年报：",companycode,'......总计：',len(codes))
	links = getpdflink(companycode)
	for name,url in links.items():
		content = requests.get(url).content
		writeFile(name,content)

# links = getpdflink('600815')
# for name,url in links.items():
# 	content = requests.get(url).content
# 	writeFile(name,content)