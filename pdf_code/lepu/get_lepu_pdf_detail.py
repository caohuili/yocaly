import pprint,os,re
import MySQLdb
#from run_result_file import lepu_text_dict
from run_result_file import patientid_dict

def get_sql_text(patientid):
	conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', password='12345678', db='ai_yocaly',charset='utf8')
	cur = conn.cursor()

	sql = "select aipdfText from ai_pdf where patientID = '%s' and aipdfDate='jw-I_compare_4'" %(patientid)
	cur.execute(sql)
	text=cur.fetchone()[0]
	cur.close()
	conn.close()
	return text


def get_sql_lepu_pdf_detail_dict():

    tag = ['平均心率(bpm)','最大心率(bpm)','最小心率(bpm)','总心搏数','房扑-房颤(占总心搏)%','最长RR间期(s)','室上性总数','室上早数','成对室上早数','二联律数','三联律数','房性逸搏数','交界性逸搏数','室性总数','室早数','成对室早数','二联律数','三联律数','室性逸搏数']
    tag_re = ['平均心率\(bpm\)','最大心率\(bpm\)','最小心率\(bpm\)','总心搏数','房扑-房颤\(占总心搏\)%','最长RR间期\(s\)','室上性总数','室上早数','成对室上早数','二联律数','三联律数','房性逸搏数','交界性逸搏数','室性总数','室早数','成对室早数','二联律数','三联律数','室性逸搏数']
    #end_tag = ['总心搏数','发生时间','发生时间','最大心率','心率变异性窦性心搏间标准差','发生时间','占总心搏','成对室上早数','交界性逸搏数','室上速阵数','占总心搏','室速阵数','三联律数',]
    tag_num = len(tag)

    lepu_pdf_detail_dict = {}

    patient_dict = patientid_dict.patientid_dict
    for patientid,name in patient_dict.items():
        try:

            text = get_sql_text(patientid)
        except:
            pass
        if '处理失败' in text:
            continue
        user_detail_list = []
        #print(name)
        name = name.split('.')[0]

        #提取发生时间
        time_tag='发生时间'
        time_result = re.findall( r'%s\s?(\d{2}:\d{2}:\d{2}|\d{4}-\d\d-\d\d\s?\d{2}:\d{2}:\d{2}|)' %(time_tag), text )

        #提取结论内容
        conclusion_pos_s= '结论'
        npos = text.index(conclusion_pos_s)
        conclusion = text[npos:]
        conclusion_tag_list,conclusion = get_conclusion_tag(conclusion)

        for ctag in conclusion_tag_list:
            new_ctag = '\n'+ctag+'\n'
            #print(new_tag)
            if ctag in conclusion:
                conclusion=conclusion.replace(ctag,new_ctag)
        conclusion = conclusion.split('\n')
        #print(name,conclusion)
        for t in conclusion:
            if t == '':
                conclusion.remove(t)
        print(name,conclusion)


        for i in range(tag_num):
            tag_dict = {}

            if i == 4:
                result = re.findall( r'%s(\d+\.\d+%%|\d+%%)' %(tag_re[i]), text )
                #print(result)
            else:
                result = re.findall( r'%s(\d+\.\d+|\d+)' %(tag_re[i]), text )
                #result = re.findall( r'(?<=%s).+?(?=%s)' %(tag_re[i],end_tag[i]), text )

            #print(result)
            tag_name = tag[i]
            if (i == tag_num-3) or (i == tag_num-2):
                tag_dict[tag_name] = result[1]
            else:
                tag_dict[tag_name] = result[0]
            #tag_dict[tag_name] = result[0]
            user_detail_list.append(tag_dict)
        user_detail_list.append({'结论':conclusion})

        #发生时间加入detail_dict
        #time_tag='发生时间'
        #time_result = re.findall( r'%s(\s?\d{2}:\d{2}:\d{2}|\d{4}-\d\d-\d\d\s?\d{2}:\d{2}:\d{2}|)' %(tag), text )
        user_detail_list.insert(2,{'最大心率发生时间':time_result[0]})
        user_detail_list.insert(4,{'最小心率发生时间':time_result[1]})
        user_detail_list.insert(8,{'最长RR间期发生时间':time_result[2]})

        lepu_pdf_detail_dict[name] = user_detail_list

    #print(lepu_pdf_detail_dict)

    with open (os.getcwd()+'\\run_result_file\\lepu_detail_dict.py','w',encoding='utf-8') as rf:
        rf.write('lepu_detail_dict = ' + pprint.pformat(lepu_pdf_detail_dict))


def get_lepu_pdf_detail_dict():

    tag = ['平均心率(bpm)','最大心率(bpm)','最小心率(bpm)','总心搏数','房扑-房颤(占总心搏)%','最长RR间期(s)','室上性总数','室上早数','成对室上早数','二联律数','三联律数','房性逸搏数','交界性逸搏数','室性总数','室早数','成对室早数','二联律数','三联律数','室性逸搏数']
    tag_re = ['平均心率\(bpm\)','最大心率\(bpm\)','最小心率\(bpm\)','总心搏数','房扑-房颤\(占总心搏\)%','最长RR间期\(s\)','室上性总数','室上早数','成对室上早数','二联律数','三联律数','房性逸搏数','交界性逸搏数','室性总数','室早数','成对室早数','二联律数','三联律数','室性逸搏数']
    #end_tag = ['总心搏数','发生时间','发生时间','最大心率','心率变异性窦性心搏间标准差','发生时间','占总心搏','成对室上早数','交界性逸搏数','室上速阵数','占总心搏','室速阵数','三联律数',]
    tag_num = len(tag)

    lepu_pdf_detail_dict = {}

    text_dict = lepu_text_dict.lepu_text_dict
    for name,text in text_dict.items():
        user_detail_list = []
        #print(name)
        name = name.split('.')[0]

        #提取发生时间
        time_tag='发生时间'
        time_result = re.findall( r'%s\s?(\d{2}:\d{2}:\d{2}|\d{4}-\d\d-\d\d\s?\d{2}:\d{2}:\d{2}|)' %(time_tag), text )

        #提取结论内容
        conclusion_pos_s= '结论'
        npos = text.index(conclusion_pos_s)
        conclusion = text[npos:]
        conclusion_tag_list,conclusion = get_conclusion_tag(conclusion)

        for ctag in conclusion_tag_list:
            new_ctag = '\n'+ctag+'\n'
            #print(new_tag)
            if ctag in conclusion:
                conclusion=conclusion.replace(ctag,new_ctag)
        conclusion = conclusion.split('\n')
        #print(name,conclusion)
        for t in conclusion:
            if t == '':
                conclusion.remove(t)
        print(name,conclusion)


        for i in range(tag_num):
            tag_dict = {}

            if i == 4:
                result = re.findall( r'%s(\d+\.\d+%%|\d+%%)' %(tag_re[i]), text )
                #print(result)
            else:
                result = re.findall( r'%s(\d+\.\d+|\d+)' %(tag_re[i]), text )
                #result = re.findall( r'(?<=%s).+?(?=%s)' %(tag_re[i],end_tag[i]), text )

            #print(result)
            tag_name = tag[i]
            if (i == tag_num-3) or (i == tag_num-2):
                tag_dict[tag_name] = result[1]
            else:
                tag_dict[tag_name] = result[0]
            #tag_dict[tag_name] = result[0]
            user_detail_list.append(tag_dict)
        user_detail_list.append({'结论':conclusion})

        #发生时间加入detail_dict
        #time_tag='发生时间'
        #time_result = re.findall( r'%s(\s?\d{2}:\d{2}:\d{2}|\d{4}-\d\d-\d\d\s?\d{2}:\d{2}:\d{2}|)' %(tag), text )
        user_detail_list.insert(2,{'最大心率发生时间':time_result[0]})
        user_detail_list.insert(4,{'最小心率发生时间':time_result[1]})
        user_detail_list.insert(8,{'最长RR间期发生时间':time_result[2]})

        lepu_pdf_detail_dict[name] = user_detail_list

    #print(lepu_pdf_detail_dict)

    with open (os.getcwd()+'\\run_result_file\\lepu_detail_dict.py','w',encoding='utf-8') as rf:
        rf.write('lepu_detail_dict = ' + pprint.pformat(lepu_pdf_detail_dict))



def get_conclusion_tag(str_result):
    conclusion_tags_re = ['结论：|结论:|结论','基本心律:|基本心律：|基本心律','心率:|心率：|心率','室上性心律失常:|室上性心律失常：|室上性心律失常','室性心律失常:|室性心律失常：|室性心律失常','传导阻滞:|传导阻滞：|传导阻滞','心室预激:|心室预激：|心室预激']
    conclusion_tags_re_num = len(conclusion_tags_re)
    user_detail_list = []
    #conclusion_pos_s= '结论：'
    #npos = text.index(conclusion_pos_s)
    #conclusion = text[npos:]
    text_rusult = str_result.replace('基本心率','基本心律')
    for i in range(conclusion_tags_re_num):
        conclusion_tag = re.search(r'(%s)' %(conclusion_tags_re[i]),text_rusult)
        if conclusion_tag is None:
            continue
        else:
            new_tag = conclusion_tag.group()
            new_tag = new_tag.replace(':','').replace('：','')
            user_detail_list.append(new_tag)
    return user_detail_list,text_rusult


if __name__ == '__main__':
    #pdf_file_path = 'E:\\work\\pdf\\20170804\\pdf\\'
    #yocaly_pdf_file_path = 'E:\\work\\pdf_read\\yocaly_pdf\\'
    #excel_file = 'E:\\work\\pdf_result\\result20170803.xlsx'
    get_lepu_pdf_detail_dict()
