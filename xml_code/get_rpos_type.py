import os,pprint
from xml.etree import ElementTree as ET
def get_rpos_type(path,date,cname):#cname为yocaly_download或lepu_download

	c = cname[:-9]#c为yocaly或lepu
	#up_path = os.path.dirname(os.getcwd())
	xml_file_dir=path+cname+'\\'+date+'\\'
	filenames = os.listdir(xml_file_dir)
	user_r_dict = {}
	for filename in filenames:
		if '.XML' in filename and 'B.DAT' not in filename:
			print(filename)

			tree = ET.parse(xml_file_dir+filename)
			EcgList = tree.find('EcgList')

			allrpos_list = []

			for b in EcgList.findall('B'):
				Comments = b.get('D')
				comment = Comments.split(',')
				rpos_dict = {}
				r_pos = int(comment[0])+int(comment[3])
				r_label = comment[7]
				rpos_dict[r_pos] = r_label
				allrpos_list.append(rpos_dict)
			user_r_dict[filename.split('.')[0]] = allrpos_list
		else:
			pass

			
	#return user_r_dict
	#with open('user_r_dict.py','w',encoding='utf-8') as f:
		#f.write('user_r_dict = '+pprint.pformat(user_r_dict))
	with open((os.getcwd()+'\\run_result_file\\'+c+'_r_dict.py'),'w',encoding='utf-8') as f:
		f.write(('ecg_r_dict= ')+pprint.pformat(user_r_dict))


def get_patient_rpos(path, date, cname,ykey):  # cname为yocaly_download或lepu_download

	c = cname[:-9]  # c为yocaly或lepu
	xml_file_dir = path + cname + '\\' + date + '\\'
	filenames = os.listdir(xml_file_dir)
	filename = ykey+'.XML'
	print(filename)
	allrpos_list = []
	if filename in filenames:

		tree = ET.parse(xml_file_dir + filename)
		EcgList = tree.find('EcgList')
		for b in EcgList.findall('B'):
			Comments = b.get('D')
			comment = Comments.split(',')
			rpos_dict = {}
			r_pos = int(comment[0]) + int(comment[3])
			r_label = comment[7]
			rpos_dict[r_pos] = r_label
			allrpos_list.append(rpos_dict)
	else:
		pass

	return allrpos_list

		
if __name__ == '__main__':
	date = '20170926'
	#path = 'E:\\xindian\\lepu-yocaly-xml-pdf\\'
	path='..\\..\\'
	#lepu_xml_path = 'E:\\xindian\\lepu-yocaly-xml-pdf\\lepu_download\\20170825\\xml\\'
	get_rpos_type(path,date, 'yocaly_download')#cname为yocaly_download或lepu_download
	get_rpos_type(path,date, 'lepu_download')#cname为yocaly_download或lepu_download