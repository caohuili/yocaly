import sys,os

def download_data(date):
	#下载yocaly的zip文件,并解压缩
	import download_yocaly_pdf_xml
	download_yocaly_pdf_xml.download_yocaly_zip(date)

	#文件重命名
	import yocaly_file_rename
	patient_name = yocaly_file_rename.get_patient_name(date)

	#下载乐普zip/xml文件
	import download_lepu_sftp_file
	from run_result_file import patientid_dict


	host = '10.0.3.115'
	host59 = '10.0.3.114'#主机
	port = 22 #端口
	username = 'caohuili' #用户名
	password = 'caohuili_@123' #密码
	username114 = 'product' #用户名
	password114 = 'Kanebay@123!!!' #密码

	zip_local = '..\\..\\lepu_download\\'+date+'\\'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
	xml_local = 'D:\\ScriptData\\datas\\'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
	xml_remote = '/raid/xmlout2/final/'#远程文件或目录，与本地一致，当前为linux目录格式
	xml_remote59 ='/raid/xmlout2/final/'
	#xml_remote59 = '/home/liutao/xmlout2/final/'  # 远程文件或目录，与本地一致，当前为linux目录格式
	#xml_remote2 = '/home/liutao/online_1/xmlout2/final/'  # 远程文件或目录，与本地一致，当前为linux目录格式
	zip_remote = '/raid/download_path/'
	id_dict = patientid_dict.patientid_dict

	download_lepu_sftp_file.sftp_download_zip(host,port,username,password,zip_local,zip_remote,date,id_dict)
	download_lepu_sftp_file.sftp_download_zip(host59,port,username114,password114,zip_local,zip_remote,date,id_dict)#下载

	#解压缩乐普zip和xml文件
	import lepu_extract_zip
	lepu_extract_zip.extract_zip(date)

	download_lepu_sftp_file.sftp_download_xml(host,port,username,password,xml_local,xml_remote,date,id_dict)
	download_lepu_sftp_file.sftp_download_xml(host59,port,username114,password114,xml_local,xml_remote,date,id_dict)


	#lepu xml文件备份重命名
	import lepu_xml_rename
	lepu_xml_rename.lepu_xml_rename(date)

	#不同的xml点写入excel
	from xml_code import write_rpos_label_excel
	path = '..\\..\\'
	write_rpos_label_excel.write_r_excel(path,date)

	from pdf_code.yocaly import yocaly2html
	html_path = '..\\..\\yocaly_download\\'
	yocaly2html.get_html(html_path,date)

	#生成乐普PDF报告
	import get_lepu_pdf
	get_lepu_pdf.get_lepu_pdf()

if __name__ == '__main__':
	date = '20180425'
	download_data(date)