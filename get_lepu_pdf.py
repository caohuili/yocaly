import subprocess
import os

def get_lepu_pdf():
	xml_path = 'D:\\ScriptData\\datas\\'
	html_path = "D:\\ScriptData\\LepuPDF"
	try:
		subprocess.call("D:\\ScriptData\\Release\\EcgReport.exe", shell=True)
		subprocess.call("exit 1", shell=True)
	except Exception as e:
		print(e)
		print('---------------dat转换PDF失败了------------------')
if __name__ == '__main__':
	get_lepu_pdf()
