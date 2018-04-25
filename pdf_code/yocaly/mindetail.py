import re,pprint
#from run_result_file import yocaly_text_dict

def get_min_yocaly_detail_dict(yocaly_pdf_detail_dict,user_name,text):

	#tag = ['平均心率(bpm)','最大心率(bpm)','最大心率发生时间','最小心率(bpm)','最小心率发生时间','总心搏数','房扑/房颤占时比','最长停搏','最长停搏发生时间','室上性总数','室上早','成对室上早','二联律','三联律','房性逸搏','交界性逸搏','室性总数','室早','成对室早','二联律','三联律','室性逸搏']
	tag = ['平均心率(bpm)','最大心率(bpm)','最小心率(bpm)','总心搏数','房扑/房颤占时比','最长停搏','室上性总数','室上早','成对室上早','二联律','三联律','房性逸搏','交界性逸搏','室性总数','室早','成对室早','二联律','三联律','室性逸搏']
	tag_re = ['平均心率\(bpm\)','最大心率\(bpm\)','最小心率\(bpm\)','总心搏数','房扑/房颤占时比','最长停搏','室上性总数(\(.?\d+%\))?','室上早','成对室上早','二联律','三联律','房性逸搏','交界性逸搏','室性总数(\(.?\d+%\))?','室早','成对室早','二联律','三联律','室性逸搏']
	tag_num = len(tag)
	#tag_zao = ['室上早','室早']

	#print(text)
	pos = text.index('指示与发现')
	text1 = text[:pos]
	conclusion = text[pos:]

	text1 = text1.replace('\n','').replace('  ','')
	#print(text1)
	# name_re = re.search(r'姓名:\s(\w+)|姓名:(\w+)|姓\s+名\s?:(\w+)', text1)
	# if bool(name_re):
	# 	name = name_re.group(1)
	# else:
	# 	name = re.search(r'姓名:(\w+)', text1).group(1)
	name = user_name

	user_detail_list = []

	for i in range(tag_num):
		tag_dict = {}
		tag_name = tag[i]
		#print(text1)

		if tag[i] not in text1:
			tag_dict[tag_name] = '×'

		else:
			if i == 4:
				result = re.findall( r'%s\s?(\d+\.\d+%%)' %(tag_re[i]), text1 )
				#print(result)
			elif i == 5:
				result = re.findall( r'%s\s?(\d+\.\d+)' %(tag_re[i]), text1 )
				#print(result)
			elif i == 6 or i == 13:
				result = re.findall( r'%s\s?(\d+)' %(tag_re[i]), text1 )
				result[0] = result[0][1]
				#result = re.search( r'%s\s?(\d+)' %(tag_re[i]), text1 ).group(2)
			else:
				result = re.findall( r'%s\s?(\d+)' %(tag_re[i]), text1 )
			print(result)

			if (i == tag_num-3) or (i == tag_num-2):
				tag_dict[tag_name] = result[1]
			elif ('逸搏' not in text1 and i == 7)or('逸搏' not in text1 and i == 14):
				tag_dict[tag_name] = '×'
			else:
				tag_dict[tag_name] = result[0]

		user_detail_list.append(tag_dict)


	#提取时间
	time_max = re.search( r'最大心率\(bpm\)\s?(\d+)\s+(\d\d:\d\d:\d\d)?',text1).group(2)
	time_min = re.search( r'最小心率\(bpm\)\s?(\d+)\s+(\d\d:\d\d:\d\d)?',text1).group(2)
	time_rr = re.findall( r'最长停搏\s\d+\.\d+\s(\d\d:\d\d:\d\d)',text1)
	if bool(time_rr):
		time_rrt=time_rr[0]
	else:
		time_rrt=''

	user_detail_list.insert(2,{'最大心率发生时间':time_max})
	user_detail_list.insert(4,{'最小心率发生时间':time_min})
	user_detail_list.insert(8,{'最长RR间期发生时间':time_rrt})


	if '附：' in conclusion:
		fu_pos = conclusion.index('附：')
		conclusion = conclusion[:fu_pos]

	if '报告日期' in conclusion:
		sign_pos = conclusion.index('报告日期')
		conclusion = conclusion[:sign_pos]


	if len(conclusion.replace(' ',''))<8:
		con_result = ['']
	else:

		conclusion = conclusion.replace('\n','').replace(' ','').replace('房性','室上性')
		tt = re.findall(r'\d+\.\d+', conclusion)
		#print(conclusion)
		if bool(tt):
			for i in range(len(tt)):
				conclusion = conclusion.replace(tt[i],'')
		else:
			pass

		con_result = conclusion.split('.')
		#print(con_result)
		if '基本心律：' in conclusion:
			base_pos = conclusion.index('基本心律：')
			base = re.search( r'基本心律：\s?(.+)',conclusion).group(1)
			if '平均心率' in base:
				avg_pos = base.index('平均心率')
				base_result = base[:avg_pos]
				base_result = base_result.replace(',','')
				con_result[0] = base_result

		else:	
			con_result.pop(0)
			if len(con_result) == 0:
				con_result.append('')
			con_result[0] = con_result[0][:-1]


	user_detail_list.append({'结论':con_result})
	user_detail_list.append({user_name:name})

	yocaly_pdf_detail_dict[user_name] = user_detail_list



if __name__ == '__main__':
	detail_dict = yocaly_text_dict.yocaly_text_dict
	yocaly_pdf_detail_dict = {}


	for username,text in detail_dict.items():
		if '结论' not in text:
			try:
				get_min_yocaly_detail_dict(yocaly_pdf_detail_dict,username,text)
			except Exception as e:
				print(e)
			print(username+'------------')

	#with open('yocaly_500_detail_dict1.py','w',encoding='utf-8') as f:
		#f.write('yocaly_500_detail_dict1 = ' + pprint.pformat(yocaly_pdf_detail_dict))
	#with open('yocaly_500_detail_dict333.py','w',encoding='utf-8') as f:
		#f.write('yocaly_500_detail_dict333 = ' + pprint.pformat(yocaly_pdf_detail_dict))

	#print(yocaly_pdf_detail_dict)
	'''

	id = 'DBD7FC23761B3553980FA71C9A6F31EEB'
	text = detail_dict[id]
	get_min_yocaly_detail_dict(yocaly_pdf_detail_dict,text)
	'''