
date = '20180306'

# from pdf_code.yocaly import yocaly2html
# html_path = '..\\..\\yocaly_download\\'
# yocaly2html.get_html(html_path,date)
#=================================================================
#
# from pdf_code.yocaly import get_yocaly_text
# get_yocaly_text.get_yocaly_text_dict(date)
#
#
# from pdf_code.lepu import get_lepu_pdf_text_dict
# pdf_file_path = 'D:\\ScriptData\\LepuPDF\\'
# get_lepu_pdf_text_dict.get_lepu_pdf_text_dict(pdf_file_path)


#=================================================================

from end_run import copy_pdf
copy_pdf(date)

from sql import yocaly_pdf_insert_data
yocaly_pdf_insert_data.yocaly_pdf_insert_data(int(date))


from sql import ai_pdf_insert_data
ai_pdf_insert_data.ai_pdf_insert_data(int(date))


from pdf_code.yocaly import get_yocaly_detail
get_yocaly_detail.get_sql_yocaly_detail()


from pdf_code.lepu import get_lepu_pdf_detail
get_lepu_pdf_detail.get_sql_lepu_pdf_detail_dict()

from pdf_code.yocaly import yocaly_write_detail_excel
modle_excel = 'pdf_code\\pdf_result.xlsx'
file_excel = 'run_result_file\\yocaly_pdf_detail.xlsx'
yocaly_write_detail_excel.yocaly_write_detail_excel(modle_excel,file_excel)

from pdf_code.lepu import lepu_write_detail_excel
excel_path = 'run_result_file\\'
before_excel_file = excel_path + 'yocaly_pdf_detail.xlsx'
result_excel = excel_path + date + '_'+'pdf_result.xlsx'
lepu_write_detail_excel.lepu_write_detail_excel(before_excel_file,result_excel,date)