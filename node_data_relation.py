import json

# 节点关系字典
relation_data={}

# 读取data_union文件
def read_union_data(file):
    with open("Data/unionData/"+file, mode="r", encoding="utf-8") as f:
        data=json.load(f)
    return data

# 构建父子节点关系
def make_child_relation():
    global relation_data
    # 读取父子关系
    ori_child_data=read_union_data("child_data_union.json")
    # 构建父子关系
    parent_child=[]
    for key, item in ori_child_data.items():
        for value in item:
            parent_child.append({"parent":key, "child":value})
    relation_data["parent_child"]=parent_child
    print("父子关系构造完成")

# 构造其他关系
def make_other_relation(relation):
    global relation_data
    # 读取文件
    item_data=read_union_data(relation+"_data_union.json")
    item_data=item_data["id"]
    word_data=read_union_data("word_data_union.json")
    # 构造item间的关系
    relationList=[]
    for key, item in item_data.items():
        for value in item:
            relationList.append({"from":key,"to":value})
    # 构造item和word之间的关系
    for key, item in word_data.items():
        if relation in item:
            for value in item[relation]:
                relationList.append({"from":value,"to":key})
    relation_data[relation]=relationList
    print(relation+" 关系构造完成")


# 构造relation_data文件
def make_relation_data():
    global relation_data
    with open("Data/nodeData/relation_data.json", mode="w", encoding="utf-8") as f:
        json.dump(relation_data, f, ensure_ascii=False)

# 工作入口
def run():
    make_child_relation()
    make_other_relation("exclusion")
    make_other_relation("inclusion")
    make_other_relation("narrowerTerm")
    make_other_relation("synonym")
    make_relation_data()

if __name__=="__main__":
    run()