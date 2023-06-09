import json
import py2neo as neo
import py2neo.bulk as bulk 

# 数据库地址
url="http://localhost:7474/"
# 用户信息
user=("neo4j", "neo4j-spfa")
# 数据库名称
graphName="neo4j"

# 打开数据库
def openGraph():
    return neo.Graph(url, auth=user, name=graphName)

# 创建单个节点
def nodeCreate(graph, id, label, node):
    node["name"]=node["title"]
    node["id"]=id
    node=[node]
    label=set(label)
    bulk.create_nodes(graph.auto(), node, label)

# 查询单个节点（用来创建关系）
def nodeFind(graph, key):
    return neo.NodeMatcher(graph).match(id=key).first()

# 创建单个父子关系
# def parent_child_Create(graph, data):
def parent_child_Create(graph, parent, child):
    # parent=data["parent"]
    # child=data["child"]
    # parent=nodeFind(graph, parent)
    # child=nodeFind(graph, child)
    if (not parent is None) and (not child is None):
        graph.create(neo.Relationship(parent, "is parent of", child))
        graph.create(neo.Relationship(child, "is child of", parent))

# 创建单个其他关系
# def relationCreate(graph, relation, data):
def relationCreate(graph, relation, fromNode, toNode):
    # fromNode=data["from"]
    # toNode=data["to"]
    # fromNode=nodeFind(graph, fromNode)
    # toNode=nodeFind(graph, toNode)
    if (not fromNode is None) and (not toNode is None):
        graph.create(neo.Relationship(fromNode, relation, toNode))

# 创建节点，flag=item、word
def createNodes(graph, flag):
    # 读取节点信息
    with open("Data/nodeData/"+flag+"_prop_data.json", mode="r", encoding="utf-8") as f:
        props=json.load(f)
    with open("Data/nodeData/"+flag+"_label_data.json", mode="r", encoding="utf-8") as f:
        labels=json.load(f)  
    # 写入节点
    for key, item in props.items():
        nodeCreate(graph, key, labels[key], item)
        print("节点 "+key+" 已创建")

# 创建关系
def createRelations(graph):
    # 读取所有关系
    with open("Data/nodeData/relation_data.json", mode="r", encoding="utf-8") as f:
        relations=json.load(f)
    # 获取节点表
    nodes={}
    ori_arr=neo.NodeMatcher(graph).match().all()
    for node in ori_arr:
        node_props=dict(node)
        nodes[node_props["id"]]=node
    # 写入关系
    for relation, array in relations.items():
        print("当前关系 "+relation)
        if relation=="parent_child":
            print("开始写入 父子 关系")
            for data in array:
                if (data["parent"] in nodes) and (data["child"] in nodes):
                    parent_child_Create(graph, nodes[data["parent"]], nodes[data["child"]])
                    print("写入 父子 关系在 "+data["parent"]+" "+data["child"]+" 之间")
        else:
            print("开始写入 "+relation+" 关系")
            for data in array:
                if (data["from"] in nodes) and (data["to"] in nodes):
                    relationCreate(graph, relation, nodes[data["from"]], nodes[data["to"]])
                    print("写入 "+relation+" 关系在 "+data["from"]+" "+data["to"]+" 之间")
    
    # 写入关系（弃用）
    # for relation, array in relations.items():
    #     if relation=="parent_child":
    #         for data in array:
    #             parent_child_Create(graph, data)
    #     else:
    #         for data in array:
    #             relationCreate(graph, relation, data)
    #     print("关系 "+relation+" 创建完成")

# 工作入口
def run():
    graph=openGraph()
    createNodes(graph, "item")
    createNodes(graph, "word")
    createRelations(graph)

if __name__=="__main__":
    run()