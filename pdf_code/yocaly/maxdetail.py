import re,pprint
#from run_result_file import yocaly_text_dict

def get_max_yocaly_detail_dict(yocaly_pdf_detail_dict,user_name,text):

    tag = ['平均心率(bpm)','最大心率(bpm)','最小心率(bpm)','总心搏数','房扑/房颤占时比','最长停搏','室上性总数','室上早','成对室上早','二联律','三联律','房性逸搏','交界性逸搏','室性总数','室早','成对室早','二联律','三联律','室性逸搏']
    #tag_re = ['平均心率:','最快心率:','最慢心率:','心搏总数:','房扑/房颤占时比(%):','最长RR间期:','室上性心搏:','室上性节律单个:','个室上早','二联律(阵)共\d+个室上早','三联律\(阵\)共\d+个室上早','房性逸搏','交界性逸搏','室性心搏','室性节律单个:','成对共\d+个室早','二联律\(阵\)共\d+个室早','三联律\(阵\)共\d+个室早','室性逸搏']
    tag_re = ['平均心率:','最快心率:','最慢心率:','心搏总数:','房扑/房颤占时比\(%\):','最长RR间期\(m?s\):','室上性心搏(\(.?\d+%\))?:','室上性节律单个:','成对共\d+个室上早','二联律\(阵\)共\d+个室上早','三联律\(阵\)共\d+个室上早','房性逸搏','交界性逸搏','室性心搏(\(.?\d+%\))?:','室性节律单个:','成对共\d+个室早','二联律\(阵\)共\d+个室早','三联律\(阵\)共\d+个室早','室性逸搏']
    tag_num = len(tag)

    pos = text.index('结论')
    text1 = text[:pos]
    conclusion = text[pos:]

    text1 = text.replace('\n','').replace('  ','')
    print(text1)
    name = re.search(r'姓名:?：?\s?(\w+)|姓\s+名\s?:(\w+)', text1).group(1)

    user_detail_list = []

    for i in range(tag_num):
        tag_dict = {}
        tag_name = tag[i]

        if '逸搏' in tag[i]:
            tag_dict[tag_name] = '×'

        else:
            if i == 4:
                result = re.findall( r'%s\s?(\d+\.\d+)' %(tag_re[i]), text1 )
                #print(result)
            elif i == 5:
                result = re.findall( r'%s\s?(\d+\.\d+)' %(tag_re[i]), text1 )
            elif i == 6 or i == 13:
                result = re.findall( r'%s\s?(\d+)' %(tag_re[i]), text1 )
                result[0] = result[0][1]
                #print(result)
            else:
                result = re.findall( r'%s\s?(\d+)' %(tag_re[i]), text1 )


            print(result[0])

            tag_dict[tag_name] = result[0]

        user_detail_list.append(tag_dict)


    #提取时间
    time_max = re.search( r'最快心率:\s?(\d+)/(\d\d:\d\d:\d\d)',text1).group(2)
    time_min = re.search( r'最慢心率:\s?(\d+)/(\d\d:\d\d:\d\d)',text1).group(2)
    rr = re.search( r'停搏停搏大于2.0秒\s(\d+)最长停搏\s(.+)QT最大QT',text1)
    if rr.group(1) != '0':
        user_detail_list[5]['最长停搏'] = rr.group(2)[:-9]
        time_rr = rr.group(2)[-8:]
    else:
        time_rr = ''

    user_detail_list.insert(2,{'最大心率发生时间':time_max})
    user_detail_list.insert(4,{'最小心率发生时间':time_min})
    user_detail_list.insert(8,{'最长RR间期发生时间':time_rr})
    #user_detail_list.append({'结论':conclusion})


    if '附：' in conclusion:
        fu_pos = conclusion.index('附：')
        conclusion = conclusion[:fu_pos]

    if '医师签名' in conclusion:
        sign_pos = conclusion.index('医师签名')
        conclusion = conclusion[:sign_pos]

    tt = re.findall(r'\d+\.\d+', conclusion)
    if bool(tt):
        for i in range(len(tt)):
            conclusion = conclusion.replace(tt[i],'')
    else:
        pass

    if len(conclusion.replace(' ',''))<8:
        con_result = ['']
    else:
        if '基本心律：' in conclusion:
            con_result = conclusion.split('\n')
            base_pos = conclusion.index('基本心律：')
            base = re.search( r'基本心律：\s?(.+)',text1).group(1)
            if '平均心率' in base:
                avg_pos = base.index('平均心率')
                base_result = base[:avg_pos]
                base_result = base_result.replace(',','')
                con_result[0] = base_result
                #con_result.insert(0,base_result)
            else:con_result[0] = base

        else:
            conclusion = conclusion.replace('\n','')
            con_result = conclusion.split('.')
            con_result.pop(0)

    user_detail_list.append({'结论':con_result})
    user_detail_list.append({user_name:name})
    yocaly_pdf_detail_dict[user_name] = user_detail_list

    print(user_detail_list)


if __name__ == '__main__':
    detail_dict = yocaly_500_text_dict.yocaly_500_text_dict
    yocaly_pdf_detail_dict = {}
    for id,text in detail_dict.items():
        if '患者信息' in text:
            try:
                get_max_yocaly_detail_dict(yocaly_pdf_detail_dict,text)
            except Exception as e:
                print(e+'eeeeeeeeeeeeeeeeee')
            print('-----------------------------')
            
    with open('yocaly_500_detail_dict222.py','w',encoding='utf-8') as f:
        f.write('yocaly_500_detail_dict222 = ' + pprint.pformat(yocaly_pdf_detail_dict))
    #print(yocaly_pdf_detail_dict)
