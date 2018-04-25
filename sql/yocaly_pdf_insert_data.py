import MySQLdb,os,time
from run_result_file import patientid_dict
from selenium import webdriver


def yocaly_pdf_insert_data(date):

    conn = MySQLdb.connect(host='127.0.0.1',port = 3306,user = 'root',password = '12345678',db = 'ai_yocaly',charset='utf8')
    cur = conn.cursor()

    sql = "INSERT INTO yocaly_pdf (ypdf_id,ypdf_date,patient_id,patient_name,ypdf_text,ypdf_path) VALUES (%s,%s,%s,%s,%s,%s)"
    sql_maxid = "select max(ypdf_id) from yocaly_pdf"
    cur.execute(sql_maxid)
    #print(cur)
    i=cur.fetchone()[0]+1
    print(i)
    path = 'E:\\pdf-xml-git\\yocaly_download\\'
    ypdf_dates = os.listdir(path)


    browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    browser.implicitly_wait(30)

    all_patient = patientid_dict.patientid_dict
    #i=1462
    names=[]
    for ypdf_date in ypdf_dates:
        #if 20171130<int(ypdf_date[:8])<20171230:
        if date == int(ypdf_date[:8]):
            url = 'file:///E:/pdf-xml-git/yocaly_download/' + ypdf_date + '/yocaly2html/'
            html_path = path + ypdf_date+'\\yocaly2html\\'
            if '.zip' not in ypdf_date:
                htmls = os.listdir(html_path)
                for html in htmls:
                    html_url = url + html
                    html_name = html.split('.')[0]
                    if html_name in names:
                        pass
                    else:
                        html_id = list(all_patient.keys())[list(all_patient.values()).index(html_name)]
                        try:
                            html_url = url + html
                            name = html.split('.')[0]
                            print(name)
                            browser.get(html_url)
                            page1 = browser.find_element_by_xpath('//*[@id="pf1"]/div[1]')
                            time.sleep(0.5)
                            # print(page1.text)
                            user_text = page1.text
                            user_text = user_text.replace('II', 'Ⅱ').replace('I', 'Ⅰ')

                            sql_data = (i,ypdf_date,html_id,html_name,user_text,html_url)
                            cur.execute(sql, sql_data)
                            i+=1
                            #cur.close()
                            conn.commit()
                            #conn.close()



                        except Exception as e:
                            print(e)
        else:
            pass
    cur.close()
    conn.commit()
    conn.close()
    browser.close()


if __name__ == '__main__':
    date =20171205
    yocaly_pdf_insert_data(date)