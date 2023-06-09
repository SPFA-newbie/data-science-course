import json

def notes_of_word_label():
###############################################
# Word标签列表：
#       1       word 名词（基本节点）
###############################################
    return None

# word节点原始数据
ori_word_data={}
# word节点标签数据
word_label_data={}
# word节点属性数据
word_prop_data={}

# 获取word_data_union中的数据
def read_union_data():
    global ori_word_data
    with open("Data/unionData/word_data_union.json", mode="r", encoding="utf-8") as f:
        ori_word_data=json.load(f)

# 构造word节点标签文件
def make_label_data():
    global ori_word_data
    global word_label_data
    for key in ori_word_data.keys():
        word_label_data[key]=["word"]
    with open("Data/nodeData/word_label_data.json", mode="w", encoding="utf-8") as f:
        json.dump(word_label_data, f, ensure_ascii=False)

# 构造word节点属性文件
def get_word_prop():
    global ori_word_data
    global word_prop_data
    for key, item in ori_word_data.items():
        word_prop_data[key]={
            "title": item["word"],
            "translate": item["translate"]
        }
    with open("Data/nodeData/word_prop_data.json", mode="w", encoding="utf-8") as f:
        json.dump(word_prop_data, f, ensure_ascii=False)

# 工作入口
def run():
    read_union_data()
    make_label_data()
    get_word_prop()

if __name__=="__main__":
    run()