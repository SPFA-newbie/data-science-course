import original_data_getter
import item_data_union
import word_data_union
import item_data_node
import word_data_node
import node_data_relation
import graph_maker

# 使用WHO的ICD-API获取原始数据
## 需要约20小时，增加线程数可以提速
## 得到oriData文件夹的内容
## 需要提供一个WHO的ICD-API的账号
original_data_getter.run()

# 将oriData文件整合为unionData文件
## 需要很短时间
## 得到unionData文件夹的内容
item_data_union.run()
word_data_union.run()

# 将unionData文件转换成为节点文件(node)和关系文件(relation)
## 需要很短时间
## 得到nodeData文件夹的内容
## 这些数据的格式是为写入Neo4j数据库设计的
item_data_node.run()
word_data_node.run()
node_data_relation.run()

# 将nodeData文件写入到Neo4j数据库中
## 需要很短时间
## 需要提供数据库的地址、名称和用户名密码
graph_maker.run()