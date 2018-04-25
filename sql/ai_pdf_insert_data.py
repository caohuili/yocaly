import MySQLdb,os,time
import PyPDF2
from run_result_file import patientid_dict

def get_lepu_pdf_text_dict(pdf_file_path,pdf_name):
    try:
        pdf_file = open(pdf_file_path+pdf_name,'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        page_one = pdf_reader.getPage(0)
        content = page_one.extractText()
        text1 = content.encode('windows-1252').decode('gbk')


        page_two = pdf_reader.getPage(1)
        content_2 = page_two.extractText()
        text2 = content_2.encode('windows-1252').decode('gbk')


        flag_end = '时间：'
        pos_e = text2.index(flag_end)
        #print(pos_e)
        text2 = text2[7:pos_e]
        result = text1+text2

        print(pdf_name+'处理成功！')

    except Exception as e:
        result = '处理失败'
        print('%s处理失败' %(pdf_name),e)
    return result


def ai_pdf_insert_data(date):

    conn = MySQLdb.connect(host='127.0.0.1',port = 3306,user = 'root',password = '12345678',db = 'ai_yocaly',charset='utf8')
    cur = conn.cursor()

    sql = "INSERT INTO ai_pdf (aipdfID,patientID,aipdfDate,scriptDate,patientName,aipdfPath,aipdfText) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    sql_maxid ="select max(aipdfID) from ai_pdf"
    cur.execute(sql_maxid)
    i=cur.fetchone()[0]+1
    path = 'E:\\pdf-xml-git\\lepu_download\\'
    aipdf_dates = os.listdir(path)

    all_patient = patientid_dict.patientid_dict
    #i=1035
    name_jy =['丁小婷', '付邦文', '侯秀芳', '倪守常', '全玉书', '冯殿玉', '刘余生', '刘振华', '刘桂花', '吉云祥', '吴九娣', '周林新', '唐世兰', '孙广德', '彭朝军', '徐根梅', '徐福喜', '朱付青', '朱守禄', '朱家东', '朱秀英', '李丽琼', '李会敏', '李先林', '李建美', '李懿庄', '李立华', '李纳', '林方淞', '潘永泉', '熊美秀', '王秀娟', '王银妹', '罗洛', '胡才刚', '葛玉华', '董小云', '蔡新民', '谢成阶', '谢金钩', '赵运丰1', '邱凤', '金友福', '陈冬和', '陈朝元', '韩骐燕', '马建民', '魏文博', '黄长牙', '龚道玲']
    for aipdf_date in aipdf_dates:
        #if 20171130<int(aipdf_date[:8])<20171229:
        if date== int(aipdf_date[:8]):
            pdf_path = path + aipdf_date+'\\'
            files = os.listdir(pdf_path)
            #files=['张雪姩_全流程.pdf']
            for file in files:
                if '.pdf' in file:
                    pdf_name = file[:-8].replace(' ','')
                    if pdf_name not in name_jy:
                        continue
                    pdf_id = list(all_patient.keys())[list(all_patient.values()).index(pdf_name)]
                    ai_text = get_lepu_pdf_text_dict(pdf_path, file)
                    ai_text = ai_text.replace('II', 'Ⅱ').replace('I', 'Ⅰ')
                    aipdf_date = 'jw-II_compare_4'
                    sql_data = (i,pdf_id,aipdf_date,'2018-03-06',pdf_name,pdf_path+file,ai_text)
                    cur.execute(sql, sql_data)
                    i+=1
                    #cur.close()
                    conn.commit()
                    #conn.close()

        else:
            pass
    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    date = 20180112
    ai_pdf_insert_data(date)