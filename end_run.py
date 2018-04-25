import os,shutil
from run_result_file import patientid_dict

def copy_pdf(date):
	lepu_pdf_path = 'D:\\ScriptData\\LepuPDF\\'
	dst_dir = '..\\..\\lepu_download\\'
	dst_path = dst_dir + date +'\\'
	users = patientid_dict.patientid_dict
	for fileid,user in users.items():
		print(user)
		filename=user+'_全流程.pdf'
		if filename in os.listdir(lepu_pdf_path):
			shutil.move(lepu_pdf_path+filename, dst_path)
		else:
			continue


def copy_result(date):
	result_path = os.getcwd() + '\\run_result_file\\'
	files = os.listdir(result_path)
	dst_path = '..\\..\\run_result_file\\'+date+'\\'
	if not os.path.exists(dst_path):
		os.mkdir(dst_path)
	for file in files:
		if '.' in file:
			print(file)
			shutil.move(result_path+file, dst_path)


if __name__ == '__main__':
	date='20180118'
	copy_pdf(date)
	copy_result(date)