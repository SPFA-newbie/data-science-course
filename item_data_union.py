import json
import csv
import os

# 没有翻译标志
Untranslated="[No translation available]"
# 全部数据
all_data={}

# 获取全部原始数据
def read_ori_data():
    global Untranslated
    global all_data
    rootPath="Data/oriData/"
    for root, ds, fs in os.walk(rootPath):
        for f in fs:
            with open(os.path.join(root, f), mode="r", encoding="utf-8") as data:
                id=f[:-5]
                all_data[id]=json.load(data)
                if all_data[id]["title"].count(Untranslated)!=0:
                    all_data[id]["title"]=all_data[id]["titleEN"]
                print("节点 "+id+" 已读取")

# 将原始数据全部保存到一个文件中
def make_union_origin():
    global all_data
    with open("Data/unionData/original_data_union.json", mode="w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False)

# 保存属性
def make_union_prop():
    
    # 获取单条属性
    def get_prop(data, prop):
        if "zh" in item[prop]:
            return (data[prop]["zh"], data[prop]["en"])
        elif "en" in item[prop]:
            return ("", data[prop]["en"])
        else:
            return ("","")
    
    global all_data
    with open("Data/unionData/prop_data_union.csv", mode="w", encoding="utf-8", newline="") as f:
        out=csv.writer(f)
        out.writerow(("id", "title", "titleEN", "definition", "definitionEN",
                      "longDefinition", "longDefinitionEN", 
                      "fullySpecifiedName", "fullySpecifiedNameEN", 
                      "diagnosticCriteria", "diagnosticCriteriaEN"))
        for key, item in all_data.items():
            part1=(key, item["title"], item["titleEN"])
            part2=get_prop(item, "definition")
            part3=get_prop(item, "longDefinition")
            part4=get_prop(item, "fullySpecifiedName")
            part5=get_prop(item, "diagnosticCriteria")
            out.writerow(part1+part2+part3+part4+part5)
            print(key+" 的属性已经写入文件")

# 保存全部的父子关系
def make_union_child():
    global all_data

    child_arr={}
    for key, item in all_data.items():
        if len(item["child"])!=0:
            child_arr[key]=item["child"]
        print("已获取 "+key+" 的孩子节点数据")

    with open("Data/unionData/child_data_union.json", mode="w", encoding="utf-8") as f:
        json.dump(child_arr, f, ensure_ascii=False)

# 保存全部其他列表关系        
def make_union_relation(relation):
    global all_data
    relations={"name":{}, "id":{}}
    for key, item in all_data.items():
        if len(item[relation])!=0:
            # # 去除未翻译标记
            # for it in item[relation]:
            #     if it.count(Untranslated)!=0:
            #         it=it[:-27]
            relations["name"][key]=item[relation]
        if len(item[relation+"ID"])!=0:
            relations["id"][key]=item[relation+"ID"]
        print("已获取 "+key+" 的 "+relation+"属性值")
    with open("Data/unionData/"+relation+"_data_union.json", mode="w", encoding="utf-8") as f:
        json.dump(relations, f,  ensure_ascii=False)

# 工作入口
def run():
    read_ori_data()
    make_union_origin()
    make_union_child()
    make_union_prop()
    make_union_relation("inclusion")
    make_union_relation("exclusion")
    make_union_relation("synonym")
    make_union_relation("narrowerTerm")

if __name__=="__main__":
    run()