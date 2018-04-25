import re,os,pprint
import MySQLdb
#from run_result_file import yocaly_text_dict
from run_result_file import patientid_dict
from pdf_code.yocaly import maxdetail,mindetail


def get_sql_text(patientid):
	conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', password='12345678', db='ai_yocaly',charset='utf8')
	cur = conn.cursor()

	sql = "select ypdf_text from yocaly_pdf where patient_id = '%s'" %(patientid)

	cur.execute(sql)
	try:
		text=cur.fetchone()[0]
	except:
		text=''
	cur.close()
	conn.close()
	return text


def get_sql_yocaly_detail():
	patient_dict = patientid_dict.patientid_dict
	yocaly_pdf_detail_dict = {}
	for patientid, user_name in patient_dict.items():
		text = get_sql_text(patientid)
		if '患者信息' in text:
			try:
				maxdetail.get_max_yocaly_detail_dict(yocaly_pdf_detail_dict, user_name, text)
			except Exception as e:
				print(e + 'maxeeeeeeeeeeeeeeeeee')
			print(user_name + '-----------------------------')
		elif text=='':
			continue

		if '结论' not in text:
			try:
				mindetail.get_min_yocaly_detail_dict(yocaly_pdf_detail_dict, user_name, text)
			except Exception as e:
				print(e + 'mineeeeeeeeeeeeeeeeee')
			print(user_name + '------------')
		elif text=='':
			continue

	with open(os.getcwd() + '\\run_result_file\\yocaly_detail_dict.py', 'w', encoding='utf-8') as f:
		f.write('yocaly_detail_dict = ' + pprint.pformat(yocaly_pdf_detail_dict))

def get_yocaly_detail():
	text_dict = yocaly_text_dict.yocaly_text_dict
	yocaly_pdf_detail_dict = {}
	for user_name,text in text_dict.items():
		if '患者信息' in text:
			try:
				maxdetail.get_max_yocaly_detail_dict(yocaly_pdf_detail_dict,user_name,text)
			except Exception as e:
				print(e+'maxeeeeeeeeeeeeeeeeee')
			print(user_name+'-----------------------------')
		if '结论' not in text:
				try:
					mindetail.get_min_yocaly_detail_dict(yocaly_pdf_detail_dict,user_name,text)
				except Exception as e:
					print(e+'mineeeeeeeeeeeeeeeeee')
				print(user_name+'------------')
			
	with open(os.getcwd()+'\\run_result_file\\yocaly_detail_dict.py','w',encoding='utf-8') as f:
		f.write('yocaly_detail_dict = ' + pprint.pformat(yocaly_pdf_detail_dict))

def get_bingshi():
	detail_dict = yocaly_text_dict.yocaly_text_dict
	for id,text in detail_dict.items():

		if '病史' in text:
			name = re.search(r'姓    名: ([^\s])+', text).group(0)
			name = name.replace('姓    名: ','')
			content = re.search(r'现病史:         (.+)', text)
			if content is None:
				content = ''
			else:
				content = content.group(1)
				content = content.replace(' ','')

			print(name,content)


if __name__ == '__main__':
	get_yocaly_detail()