import subprocess
import os

def get_html(html_path,date):
	path = html_path+date+'\\'
	#print(path)
	user_names = os.listdir(path)
	num = len(user_names)
	i=0
	for user_name in user_names:
		if '.XML' in user_name:
		    user_name = user_name.split('.')[0]

		    filename = path + user_name
		    i += 1
		    #name = file_name.split('.')[0]
		    #subprocess.call("D:\\pdf2html\\pdf2htmlEX.exe "+filename+".pdf --first-page 1 --last-page 1 "+user_name+".html", shell=True)
		    try:
		    	subprocess.call("D:\\pdf2html\\pdf2htmlEX.exe "+filename+".pdf --first-page 1 --last-page 1 --dest-dir "+path+"yocaly2html "+user_name+".html", shell=True)
		    	print(user_name,i,'/',num,'--------------------------')
		    except Exception as e:
		    	print(e)
		    	print('---------------%s失败了------------------' %(filename))
if __name__ == '__main__':
	date = '20170930'
	html_path = '..\\..\\..\\..\\yocaly_download\\'
	get_html(html_path,date)