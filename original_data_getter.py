import threading
import requests
import urllib3
import json
import os

# Token
token=""
# 全局字典
ICD_dict={}
# 基础URL
baseURL="https://id.who.int/icd/entity/"
# 没有翻译标志
Untranslated=" [No translation available]"
# 线程数量
threadingNum=0
maxThreadingNum=30
# 线程锁
tnLock=threading.Lock()
dictLock=threading.Lock()

# URL处理
def id_to_url(id):
    return baseURL+id
def url_to_id(url):# 只适用于http
    return url[29:]

# 获取token
def get_token():
    global token
    token_endpoint="https://icdaccessmanagement.who.int/connect/token"
    token_data={
        "client_id":"29c28af7-e2d5-45cb-82b3-44cdfa874f2a_3e429909-04d6-4782-a6df-ce598c425eb7",
        "client_secret":"Ee/X8iBkKZzLA29s9e3eCATFjQP3Qke5BtjGLqmHb0E=",
        "grant_type":"client_credentials",
        "scope":"icdapi_access",
    }
    token=requests.post(token_endpoint, data=token_data, verify=False).json()
    token=token["access_token"]

# 获取数据
def get_zh_data(url, token):
    header={
        "Authorization":"Bearer "+token,
        "Accept":"application/json",
        "Accept-Language":"zh",
        "API-Version":"v2"
    }
    result=requests.get(url, headers=header, verify=False).json()
    return result

def get_en_data(url, token):
    header={
        "Authorization":"Bearer "+token,
        "Accept":"application/json",
        "Accept-Language":"en",
        "API-Version":"v2"
    }
    result=requests.get(url, headers=header, verify=False).json()
    return result

# 条目生成
def item_maker(zh_data, en_data):

    def props_maker(zh_data, en_data, prop_name):
        global Untranslated
        prop={}
        if prop_name in en_data:
            prop["en"]=en_data[prop_name]["@value"]
        if prop_name in zh_data:
            if zh_data[prop_name]["@value"].count(Untranslated)==0:
                prop["zh"]=zh_data[prop_name]["@value"]
        return prop
    
    # 列表不记录英文内容
    def list_maker(zh_data, list_name):
        id_list=[]
        name_list=[]
        if list_name in zh_data:
            for item in zh_data[list_name]:
                if "foundationReference" in item:
                    id_list.append(url_to_id(item["foundationReference"]))
                else:
                    name_list.append(item["label"]["@value"])
        return name_list, id_list

    data={}
    data["title"]=""
    data["titleEN"]=""
    if "title" in zh_data: data["title"]=zh_data["title"]["@value"]
    if "title" in en_data: data["titleEN"]=en_data["title"]["@value"]

    data["definition"]=props_maker(zh_data, en_data, "definition")
    data["longDefinition"]=props_maker(zh_data, en_data, "longDefinition")
    data["fullySpecifiedName"]=props_maker(zh_data, en_data, "fullySpecifiedName")
    data["diagnosticCriteria"]=props_maker(zh_data, en_data, "diagnosticCriteria")

    data["inclusion"], data["inclusionID"]=list_maker(zh_data, "inclusion")
    data["exclusion"], data["exclusionID"]=list_maker(zh_data, "exclusion")
    data["synonym"], data["synonymID"]=list_maker(zh_data, "synonym")
    data["narrowerTerm"], data["narrowerTermID"]=list_maker(zh_data, "narrowerTerm")

    data["child"]=[]
    if "child" in zh_data:
        for url in zh_data["child"]:
            data["child"].append(url_to_id(url))
    data["parent"]=[]
    if "parent" in zh_data:
        for url in zh_data["parent"]:
            data["parent"].append(url_to_id(url))

    return data

# 递归查值
def data_DFS(id):
    global token
    global ICD_dict
    global threadingNum
    global maxThreadingNum

    dictLock.acquire()
    if not id in ICD_dict:
        ICD_dict[id]={}
        dictLock.release()
        url=id_to_url(id)
        finish=0
        while(finish<3):
            try:
                zh_data=get_zh_data(url, token)
                en_data=get_en_data(url, token)
                finish=10
            except:
                print("重新获取token")
                get_token()
                finish=finish+1

        if finish==10:
            data=item_maker(zh_data, en_data)
            dictLock.acquire()
            ICD_dict[id]=data
            dictLock.release()
            with open("Data/oriData/"+id+".json", mode="w", encoding="utf-8") as ori:
                json.dump(data, ori, ensure_ascii=False)            
        else:
            dictLock.acquire()
            del ICD_dict[id]
            dictLock.release()
            with open("Data/oriData/error-"+id+".json", mode="w", encoding="utf-8") as ori:
                json.dump({}, ori, ensure_ascii=False)   
            return None
    else:
        dictLock.release()
        info="节点 "+id+" 已获取，直接进行读取"
        print(info)
        while(not "title" in ICD_dict[id]):
            a=1
        dictLock.acquire()
        data=ICD_dict[id]
        dictLock.release()

    info="开始获取 "+data["title"]+" 的子节点"
    print(info)

    threads=[]
    if len(data["child"])>0:
        for child in data["child"]:
            tnLock.acquire()
            if threadingNum<maxThreadingNum :                
                threadingNum=threadingNum+1
                print("线程数："+str(threadingNum))
                tnLock.release()
                t=threading.Thread(target=data_DFS, args=(child,))
                t.start()
                threads.append(t)
            else:
                tnLock.release()
                data_DFS(child)

    if len(threads)!=0:
        for t in threads:
            t.join()
            tnLock.acquire()
            threadingNum=threadingNum-1
            print("线程数："+str(threadingNum))
            tnLock.release()

    info=data["title"]+" 及其子节点完成"
    print(info) 
    return None    

# 断点续传, 读取已获取的数据
def get_finish_data():
    global ICD_dict
    for root, ds, fs in os.walk("Data/oriData"):
        for f in fs:
            id=f[:-5]
            with open(os.path.join(root, f), mode="r", encoding="utf-8") as data:
                ICD_dict[id]=json.load(data)
            print("已读取 "+id)

# 工作入口
def run():
    # 入口id
    root_id="448895267"

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    get_finish_data()
    get_token()
    data_DFS(root_id)

if __name__=="__main__":
    run()