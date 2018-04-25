import shutil,os,sys
sys.path.append('..\\..')
from run_result_file import patientid_dict
def lepu_xml_rename(date):
	lepu_xml_path = '..\\..\\lepu_download\\'+date+'\\'
	xml_copy(date, lepu_xml_path)
	id_name = patientid_dict.patientid_dict
	
	filenames = os.listdir(lepu_xml_path)
	for k,name in id_name.items():
		filename = k+'B.DAT.XML'
		new_filename = name+'.XML'
		if filename in filenames and new_filename not in filenames:
			os.rename(lepu_xml_path+filename,lepu_xml_path+id_name[k]+'.XML')
	xml_copy(date, lepu_xml_path)


def xml_copy(date,dst_path):
	xml_path = 'D:\\ScriptData\\datas\\'
	filenames = os.listdir(xml_path)
	id_name = patientid_dict.patientid_dict
	#dst_path='E:\\xindian\\lepu-yocaly-xml-pdf\\lepu_download\\'+date+'\\'
	for filename in filenames:
		userid = filename.split('.')[0][:-1]
		if ('.XML' in filename) and (userid in id_name):
			print(userid)
			shutil.copy(xml_path+filename,dst_path)

if __name__ == '__main__':
	date='20171117'
	#lepu_xml_rename(date)
	dst_path = 'E:\\pdf-xml-git\\lepu_download\\'+date+'\\'
	xml_copy(date, dst_path)