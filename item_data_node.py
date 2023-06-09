import json

def notes_of_item_label():
###############################################
# Item标签列表：
#       1       item 条目（基本节点）
#       1.1     catalog 目录（有子节点）
#       1.2     leaf 叶子节点（没有子节点）
#       1.3     basic 基本条目
#       1.4     supply 功能评定补充部分
#       1.5     extend 扩展码
#       1.6     root 总括条目（入口、根条目）
###############################################
    return None

# 特殊ID
sp_dict={
    "item":"448895267", # 入口
    "basic":"455013390", # 主目录
    "extend":"1920852714", # 扩展码
    "supply":"231358748"# 功能评定补充部分
}
# 注释标志
possible_translation="[possible translation]"
no_translation="[No translation available]"
# item节点标签表
item_node_label={}
# item节点属性表
item_node_data={}
# 子节点映射，从unionData/child_data_union.json中读取
child_data={}

# 读取数据
def read_data(file):
    with open("Data/unionData/"+file, mode="r", encoding="utf-8") as f:
        data=json.load(f)
    return data

# 为节点给予标签
def set_label(id, label):
    global item_node_label
    if not id in item_node_label:
        item_node_label[id]=[]
    if type(label)==str:
        if item_node_label[id].count(label)==0:
            item_node_label[id].append(label)
    else:
        for aLabel in label:
            if item_node_label[id].count(aLabel)==0:
                item_node_label[id].append(aLabel)

# 特殊条目检定
def special_check(id):
    global sp_dict
    for key, item in sp_dict.items():
        if id==item:
            return True, key
    return False, ""

# 搜索条目节点，标记节点是不是叶子节点
def item_node_DFS(id, labelList):
    global child_data
    
    nowLabelList=labelList.copy()
    is_root, label=special_check(id)
    if is_root==True:
        nowLabelList.append(label)
        set_label(id, "root")
        if label=="supply":
            nowLabelList.remove("basic")

    set_label(id, nowLabelList)
    if id in child_data:
        set_label(id, "catalog")
        for child in child_data[id]:
            item_node_DFS(child, nowLabelList)
    else:
        set_label(id, "leaf")
    print(id+" 节点的标签设置完成")

# 创建item节点的标签文件
def make_item_label_data():
    global item_node_label
    with open("Data/nodeData/item_label_data.json", mode="w", encoding="utf-8") as f:
        json.dump(item_node_label, f, ensure_ascii=False)

# 构造节点标签列表
def label_make():
    global child_data
    child_data=read_data("child_data_union.json")
    item_node_DFS(sp_dict["item"], [])
    make_item_label_data()

# 获取所有item节点的属性
def node_prop_getter():
    # 获取节点单条属性
    def get_prop(data, prop):
        if "zh" in item[prop]:
            return data[prop]["zh"], data[prop]["en"]
        elif "en" in item[prop]:
            return "", data[prop]["en"]
        else:
            return "",""
    # 开始获取
    global item_node_data
    global no_translation
    global possible_translation
    props=["definition","longDefinition","fullySpecifiedName","diagnosticCriteria"]
    ori_data=read_data("original_data_union.json")
    for key, item in ori_data.items():
        item_node_data[key]={}
        item_node_data[key]["title"]=""
        item_node_data[key]["titleEN"]=""
        # 处理标题未翻译的问题
        item_node_data[key]["titleTranslate"]="definite"
        if item["title"].count(no_translation)!=0:
            item["title"]=item["titleEN"]
            item_node_data[key]["titleTranslate"]="absent"
        elif item["title"].count(possible_translation)!=0:
            item["title"]=item["titleEN"]
            item_node_data[key]["titleTranslate"]="indefinite"
        # 获取标题
        item_node_data[key]["title"]=item["title"]
        item_node_data[key]["titleEN"]=item["titleEN"]
        # 获取其他属性
        for prop in props:
            item_node_data[key][prop], item_node_data[key][prop+"EN"]=get_prop(item, prop)
        
# 将item节点的属性写到文件中
def make_item_prop_data():
    global item_node_data
    with open("Data/nodeData/item_prop_data.json", mode="w", encoding="utf-8") as f:
        json.dump(item_node_data, f, ensure_ascii=False)

# 构造节点属性列表
def prop_make():
    node_prop_getter()
    make_item_prop_data()


# 工作入口
def run():
    label_make()
    prop_make()

if __name__=="__main__":
    run()