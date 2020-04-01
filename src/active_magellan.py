# -*- coding: UTF-8 -*-
#!/bin/python
# Invoke this script from /root

import sys
sys.path.append('/magellan/py_entitymatching/py_entitymatching/')


import py_entitymatching as em
import pandas as pd
import os
import numpy as np

path_A = em.get_install_path() + os.sep + 'datasets' + os.sep + 'end-to-end' + os.sep + 'restaurants/fodors.csv'
path_B = em.get_install_path() + os.sep + 'datasets' + os.sep + 'end-to-end' + os.sep + 'restaurants/zagats.csv'
A = em.read_csv_metadata(path_A, key='id')
B = em.read_csv_metadata(path_B, key='id')

print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A)*len(B)))

ob = em.OverlapBlocker()
C = ob.block_tables(A, B, 'name', 'name', 
                    l_output_attrs=['name', 'addr', 'city', 'phone'], 
                    r_output_attrs=['name', 'addr', 'city', 'phone'],
                    overlap_size=1, show_progress=False
                    )
len(C)
S = em.sample_table(C, 450)


#G = em.label_table(S, 'gold') # This step raises an error


path_G = em.get_install_path() + os.sep + 'datasets' + os.sep + 'end-to-end' + os.sep + 'restaurants/lbl_restnt_wf1.csv'
#print('path is:' + path_G)
G = em.read_csv_metadata(path_G, 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_id', fk_rtable='rtable_id')
print('Length is ' + str(len(G)))

#print(G)

dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0, probability=True)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')


feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)
H = em.extract_feature_vecs(G, 
                            feature_table=feature_table, 
                            attrs_after='gold',
                            show_progress=False)

def RS(proba, batch_size):
    return np.random.choice(range(proba.shape[0]),batch_size,replace=False)

def LC(proba, batch_size):
    return np.argsort(np.max(proba,axis=1))[:batch_size]

def BT(proba, batch_size):
    sorted_proba = np.sort(proba,axis=1)
    return np.argsort(sorted_proba[:,-1]-sorted_proba[:,-2])[:batch_size]

Features = em.extract_feature_vecs(G, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)

strategies = {"RS":RS,"LC":LC,"BT":BT}
CLF = {"DecisionTree": dt, "SVM": svm, "RandomForest":rf, "LogisticRegression":lg, "LinearRegression":ln, "NaiveBayes": nb}
for clf_name in CLF:
  for strategy_name in strategies:
    clf = CLF[clf_name]
    batch_size = 10
    rounds = 5
    F = Features

    anno_batch = RS(Features,batch_size)    # 第一批标注样本只能随机选取
    train_index = anno_batch
    F = F.drop(anno_batch)
    for i in range(rounds-1):
        train_data = Features.iloc[train_index]
#        print(train_data.shape)
        clf.fit(table=train_data, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], target_attr='gold')
        predictions = clf.predict(x=F.drop(['_id', 'ltable_id', 'rtable_id', 'gold'], axis = 1), return_probs = True)
        proba = np.array([predictions[1], 1 - predictions[1]])
        proba = np.swapaxes(proba,0,1)
#        print(proba)
        anno_batch = strategies[strategy_name](proba,batch_size)
        anno_batch = F.index[anno_batch]
        train_index = np.append(train_index, anno_batch)
#        print(F, anno_batch)
        F = F.drop(anno_batch)
    clf.fit(table=train_data, 
           exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
           target_attr='gold')
    predictions = clf.predict(table=Features, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
                  append=True, target_attr='predicted', inplace=False)
    #print(predictions)
    eval_result = em.eval_matches(predictions, 'gold', 'predicted')
    print("Classifier: %s, strategy: %s" % (clf_name, strategy_name))
    print("batch_size:%d, rounds:%s" %(batch_size, rounds))
    em.print_eval_summary(eval_result)



