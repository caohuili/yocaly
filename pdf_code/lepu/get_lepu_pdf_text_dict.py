import PyPDF2
import os
import pprint


def get_lepu_pdf_text_dict(pdf_file_path):

    pdf_names = os.listdir(pdf_file_path)
    #usern=['刘余生', '李会敏', '冯殿玉', '刘桂花', '朱家东', '潘永泉', '周林新', '李丽琼', '全玉书', '刘振华', '胡才刚', '朱付青', '陈朝元', '丁小婷', '蔡新民', '邱凤', '金友福', '徐福喜', '朱守禄', '罗洛', '李纳', '马建民', '李懿庄', '龚道玲', '李建美', '陈冬和', '龚道玲2', '熊美秀', '唐世兰', '侯秀芳', '王银妹', '魏文博', '谢成阶', '李先林', '朱秀英']

    count_i = 1
    total_i = len(pdf_names)
    lepu_pdf_text_dict = {}

    for pdf_name in pdf_names:
        #if pdf_name.replace('_全流程.pdf','') in usern:

        try:
            print('开始处理第%d-%d个文件：%s' %(total_i,count_i,pdf_name))

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
            text2 = text2[7:pos_e]
            result = text1+text2

            #print(text1,text2)




            print('处理成功！')
            lepu_pdf_text_dict[pdf_name] = result
            count_i += 1

        except Exception as e:
            print('%s处理失败' %(pdf_name),e)


    #return lepu_pdf_text_dict

    with open (os.getcwd()+'\\run_result_file\\lepu_text_dict.py','w',encoding='utf-8') as rf:
        rf.write('lepu_text_dict = ' + pprint.pformat(lepu_pdf_text_dict))


if __name__ == '__main__':
    pdf_file_path = 'D:\\ScriptData\\LepuPDF\\'
    #pdf_file_path = 'E:\\xindian\\lepu-yocaly-xml-pdf\\lepu_download\\20170921-41\\'
    #lepu_pdf_text_dict = 'E:\\work\\pdf\\pdf\\lepu_pdf_text_dict.py'
    get_lepu_pdf_text_dict(pdf_file_path)