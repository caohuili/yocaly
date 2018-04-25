import pprint,os,time
from selenium import webdriver

def get_yocaly_text_dict(date):
	html_path = '..\\..\\yocaly_download\\'+date+'\\yocaly2html\\'
	url_path = os.path.abspath(os.path.join(os.getcwd(), "..\\..\\"))[3:]
	url = 'file:///E:/'+url_path+'/yocaly_download/'+date+'/yocaly2html/'


	#browser = webdriver.Firefox()
	browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
	#browser.implicitly_wait(30)
	yocaly_500_text_dict = {}

	file_names = os.listdir(html_path)

	i = 0

	#file_names =['75D44260A29F85C41FDA92B93C0F17E9B']

	for file_name in file_names:
		#file_name = file_name + '.DAT.html'


		try:
			html_url = url + file_name
			name = file_name.split('.')[0]
			print(name)
			browser.get(html_url)
			#page1 = browser.find_element_by_id('pf1')
			page1 = browser.find_element_by_xpath('//*[@id="pf1"]/div[1]')
			time.sleep(0.5)
			#print(page1.text)
			user_text = page1.text
			yocaly_500_text_dict[name] = user_text.replace('II','Ⅱ').replace('I','Ⅰ')

		except Exception as e:
			print(e)

		i += 1
		print(str(i)+'------------------------')

	with open((os.getcwd()+'\\run_result_file\\yocaly_text_dict.py'),'w',encoding='utf-8') as f:
		f.write('yocaly_text_dict = ' + pprint.pformat(yocaly_500_text_dict))

	browser.close()

if __name__ == '__main__':
	date='20170926'
	get_yocaly_text_dict(date)