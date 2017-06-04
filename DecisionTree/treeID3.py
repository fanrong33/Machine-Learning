# encoding: utf-8
'''
Decision Tree ID3
@author 蔡繁荣
@version 1.0.0 build 20170604
'''
from math import log
import operator

''' 创建数据集，是否为鱼类
'''
def create_data_set():
    data_set = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flipprs']
    return data_set, labels


''' 计算data_set中label的香农熵
'''
def calc_shannon_entropy(data_set): 
    num_entries = len(data_set) # 5条数据集
    label_counts_dict = {}
    for feat_vec in data_set: #the the number of unique elements and their occurance
        current_label = feat_vec[-1]
        if current_label not in label_counts_dict.keys(): label_counts_dict[current_label] = 0
        label_counts_dict[current_label] += 1
    shannon_entropy = 0.0
    for key in label_counts_dict:
        prob = float(label_counts_dict[key])/num_entries
        shannon_entropy -= prob * log(prob, 2) # log base 2
    return shannon_entropy


''' 划分数据集
划分出在axis位置值是value的数据
'''
def split_data_set(data_set, axis, value):
    # 1. 创建新的list对象
    ret_data_set = []
    for feat_vec in data_set:
        if feat_vec[axis] == value:
            # 2. 抽取
            reduced_feat_vec = feat_vec[:axis]
            reduced_feat_vec.extend(feat_vec[axis+1:])
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set

def choose_best_feature_to_split(data_set):
    features_num = len(data_set[0]) - 1 #the last column is used for the labels
    # print(features_num) # 2
    base_entropy = calc_shannon_entropy(data_set)
    # print(base_entropy)
    best_info_gain = 0.0 # 信息增益
    best_feature = -1
    for i in range(features_num):   #iterate over all the features
        # 1. 创建唯一的分类标签列表
        feat_list = [example[i] for example in data_set]  #create a list of all the examples of this feature
        unique_vals = set(feat_list)  #get a set of unique values
        new_entropy = 0.0
        # 2. 计算每种划分方式的信息熵
        for value in unique_vals:
            sub_data_set = split_data_set(data_set, i, value)
            prob = len(sub_data_set)/float(len(data_set))
            new_entropy += prob * calc_shannon_entropy(sub_data_set)
        info_gain = base_entropy - new_entropy    #calculate the info gain; ie reduction in entropy
        if(info_gain > best_info_gain):     #compare this to the best gain so far
            best_info_gain = info_gain      #if better than current best, set to best
            best_feature = i
    return best_feature   # returns an integer


''' 投票表决函数'''
def majority_count(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys(): 
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(),
        key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

def create_tree(data_set, labels):
    classList = [example[-1] for example in data_set]
    if classList.count(classList[0]) == len(classList): 
        return classList[0]#stop splitting when all of the classes are equal
    if len(data_set[0]) == 1: #stop splitting when there are no more features in dataSet
        return majority_count(classList)
    bestFeat = choose_best_feature_to_split(data_set)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in data_set]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = create_tree(split_data_set(data_set, bestFeat, value),subLabels)
    return myTree

''' 预测分类
'''
def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: 
        classLabel = valueOfFeat
    return classLabel

def store_tree(input_tree, filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(input_tree,fw)
    fw.close()
    

def grab_tree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)



if __name__ == '__main__':
    data_set, labels = create_data_set()
    # print(data_set)
    # [[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]

    shannon_entropy = calc_shannon_entropy(data_set)
    # print(shannon_entropy)
    # 0.970950594455

    ret_data_set = split_data_set(data_set, 0, 1)
    # print(ret_data_set)
    # [[1, 'yes'], [1, 'yes'], [0, 'no']]

    ret_data_set = split_data_set(data_set, 0, 0)
    # print(ret_data_set)
    # [[1, 'no'], [1, 'no']]


    my_tree = create_tree(data_set, labels)
    store_tree(my_tree, 'trees_saved.txt')
    print(my_tree)
    # {'no surfacing': {0: 'no', 1: {'flipprs': {0: 'no', 1: 'yes'}}}}

    print(labels) # labels 会被create_tree修改，丢失
    data_set, labels = create_data_set()

    # 预测分类
    predict_label = classify(my_tree, labels, [0, 0])
    print(predict_label)
    # no
    predict_label = classify(my_tree, labels, [1, 1])
    print(predict_label)
    # yes











