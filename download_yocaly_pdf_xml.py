import requests,sys
sys.path.append('..\\..')
import zipfile,os

def download_yocaly_zip(date):
	udate = date[:4]+'-'+date[4:6]+'-'+date[6:]
	url = 'http://58.56.56.186:31027/DOWONResult?ymd='+udate
	yocaly_zip = '..\\..\\yocaly_download\\' +date+'.zip'

	r = requests.get(url)
	if '"code":"ERROR"' in r.text:
		#print(type(r.text))
		print('yocaly还没有数据上传')
	else:
		print('开始下载yocaly数据')
		with open(yocaly_zip,'wb') as f:
			f.write(r.content)
		print('yocaly数据下载完成')
		extract_yocaly_zip(date,yocaly_zip)

def extract_yocaly_zip(date,yocaly_zip):
	zip_file = zipfile.ZipFile(yocaly_zip,'r')
	extract_path = '..\\..\\yocaly_download\\'+date+'\\'
	if os.path.exists(extract_path):
		pass
	else:
		os.makedirs(extract_path)
	for file in zip_file.namelist():
		zip_file.extract(file,extract_path)
	print(date+'.zip文件解压缩完成')


if __name__ == '__main__':
	date='20170828'
	download_yocaly_zip('20170925')