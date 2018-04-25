import zipfile,os,sys
sys.path.append('..//..')
import shutil


def extract_zip(date):
	'''
	if os.path.exists("D:\\ScriptData\\datas\\"):
		shutil.rmtree("D:\\ScriptData\\datas\\")
	else:
		os.makedirs("D:\\ScriptData\\datas\\")
	'''
	local = '..\\..\\lepu_download\\'+date+'\\'
	#local = 'E:\\xindian\\lepu-yocaly-xml-pdf\\lepu_download\\'+date+'\\'
	zipfiles = os.listdir(local)
	try:
		for zfile in zipfiles:
			if '.zip' in zfile:
				print(zfile)
				zip_file = zipfile.ZipFile(local+zfile,'r')
				for file in zip_file.namelist():
					zip_file.extract(file,"D:\\ScriptData\\datas\\")
			else:
				pass
	except Exception as e:
		print('解压缩失败：',e)

if __name__ == '__main__':
	#local = 'e:\\lepu_yocaly_xmlpdf\\sftp\\20170818\\'
	extract_zip('20170925')

