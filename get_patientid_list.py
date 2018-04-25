import os

def get_patientid_list(date):
	patientid_list = []
	path = 'E:\\xindian\\lepu-yocaly-xml-pdf\\yocaly_download\\'+date+'\\'
	filenames = os.listdir(path)
	for filename in filenames:
		if '.DAT.PDF' in filename:
			patientid_list.append(filename.split('.')[0][:-1])
	print(patientid_list)
	return patientid_list
if __name__ == '__main__':
	get_patientid_list('20170822')
