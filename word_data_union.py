import json

# 注释标志
possible_translation="[possible translation]"
no_translation="[No translation available]"
# 名词词典
word_dict={} # 名词映射属性
wid_dict={}  # 为名词分配id
# 名词ID
wid=100000

# 从data_union中读取数据，catalog=exclusion、inclusion、narrowerTerm、synonym
def read_union_data(catalog):
    global possible_translation
    global no_translation
    global word_dict
    with open("Data/unionData/"+catalog+"_data_union.json", mode="r", encoding="utf-8") as f:
        data=json.load(f)
        for id, nameList in data["name"].items():
            for name in nameList:
                # 测试条目的翻译情况
                trans=0 # 0=已翻译，1=未翻译，2=可能的翻译
                if name.count(possible_translation)!=0:
                    trans=2
                    name=name[:-23]
                elif name.count(no_translation)!=0:
                    trans=1
                    name=name[:-27]
                # 添加条目到字典
                if not name in word_dict:
                    word_dict[name]={"word":name}
                    if trans==0: 
                        word_dict[name]["translate"]="definite"
                        word_dict[name]["fullWord"]=name
                    elif trans==1: 
                        word_dict[name]["translate"]="absent"
                        word_dict[name]["fullWord"]=name+" "+no_translation
                    elif trans==2: 
                        word_dict[name]["translate"]="indefinite"
                        word_dict[name]["fullWord"]=name+" "+possible_translation
                if not catalog in word_dict[name]:
                    word_dict[name][catalog]=[]
                if word_dict[name][catalog].count(id)==0:
                    word_dict[name][catalog].append(id)

# 字典转换
def switch_dict():
    global wid
    global wid_dict
    global word_dict
    for value in word_dict.values():
        wid_dict["w"+str(wid)]=value
        wid=wid+1

# 保存union文件
def save_union():
    global wid_dict
    with open("Data/unionData/word_data_union.json", mode="w", encoding="utf-8") as f:
        json.dump(wid_dict, f, ensure_ascii=False)

# 工作入口
def run():
    read_union_data("exclusion")
    read_union_data("inclusion")
    read_union_data("narrowerTerm")
    read_union_data("synonym")
    switch_dict()
    save_union()

if __name__=="__main__":
    run()