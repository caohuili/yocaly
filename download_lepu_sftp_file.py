import paramiko
import os,sys
sys.path.append('..//..')
import time


from run_result_file import patientid_dict

def sftp_download_zip(host,port,username,password,local,remote,date,patientid_dict):
    sf = paramiko.Transport((host,port))
    sf.connect(username = username,password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    
    #patientid_list = get_patientid_list.get_patientid_list(date)

    if os.path.exists(local):
        pass
    else:
        os.makedirs(local)
    #try:
    if os.path.isdir(local):#判断本地参数是目录还是文件
        pl = list(set(patientid_dict))
        #遍历远程目录
        remotefiles=sftp.listdir(remote)
        for i in range(len(pl)):
            file_name = pl[i]+'.zip'
            if file_name in remotefiles:
                try:
                    sftp.get(os.path.join(remote+file_name),os.path.join(local+file_name))#按照id下载文件
                    print(file_name+'下载完成')
                except Exception as e:
                    continue
 
    #except Exception as e:
        #print('download zip exception:',e)

    sf.close()

def sftp_download_xml(host,port,username,password,local,remote,date,patientid_dict):
    sf = paramiko.Transport((host,port))
    sf.connect(username = username,password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)

    #try:
    if os.path.isdir(local):#判断本地参数是目录还是文件
        pl=list(set(patientid_dict))
        #遍历远程目录
        remotefiles=sftp.listdir(remote)
        for i in range(len(pl)):
            
            file_name = pl[i]+'B.DAT.XML'
            if file_name in remotefiles:
                try:
                #print(file_name)
                #print(os.path.join(remote+file_name))
                    sftp.get(os.path.join(remote+file_name),os.path.join(local+file_name))#按照id下载文件
                    print(file_name+'下载完成')
                except Exception as e:
                    continue
            else:
                pass
 
    #except Exception as e:
        #print('download xml exception:',e)
    sf.close()

if __name__ == '__main__':
    date = '20171023'
    host58 = '10.10.9.158'
    host59 = '10.10.9.159'#主机
    port = 22 #端口
    username = 'liutao' #用户名
    password = 'liutao' #密码
    zip_local = '..\\..\\lepu_download\\'+date+'\\'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
    xml_local = 'D:\\ScriptData\\datas\\'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
    xml_remote = '/home/liutao/xmlout2/final/'#远程文件或目录，与本地一致，当前为linux目录格式
    #zip_remote = '/home/liutao/download_path/'
    zip_remote = '/raid/download_path/'

    #id_dict = patientid_dict.patientid_dict

    id_dict = { 'E8CF73069E8AF3BCA054FFC92BA432FC': '李熤敏', '9D0B1256A0D5F6035B58D0782DAA6E08': '陈水香'}

    sftp_download_zip(host58,port,username,password,zip_local,zip_remote,date,id_dict)
    sftp_download_zip(host59,port,username,password,zip_local,zip_remote,date,id_dict)#下载
    sftp_download_xml(host58,port,username,password,xml_local,xml_remote,date,id_dict)
    sftp_download_xml(host59,port,username,password,xml_local,xml_remote,date,id_dict)
    #sftp_upload(host,port,username,password,local,remote)#上传SSS