#!/bin/python
'''
NOTE: Invoke this script from /root

Evaluation of dataset provided as the link_example dataset
'''

import sys
sys.path.append('/magellan/py_entitymatching/py_entitymatching/')

import py_entitymatching as em
import pandas as pd
import os
import numpy as np

path_A = '/datasets/buy_sell/MODIFIED_AbtBuy_Abt.csv'
path_B = '/datasets/buy_sell/AbtBuy_Buy.csv'
A = em.read_csv_metadata(path_A, key='id')
B = em.read_csv_metadata(path_B, key='id')

em.is_dfinfo_present(A)
em.is_dfinfo_present(B)


print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A)*len(B)))

# Replace missing values with ''
# Removes A and B from the em. catalog
A = A.replace(np.nan, '_', regex=True)
B = B.replace(np.nan, '_', regex=True)

em.set_key(A,'id')
em.set_key(B,'id')


# A.values
# list(A.values)

ob = em.OverlapBlocker()
C = ob.block_tables(A, B, 'name', 'name', 
                    l_output_attrs=['name','description','price'], 
                    r_output_attrs=['name','description','price'],
                    overlap_size=1, show_progress=True
                    )


len(C)
#S = em.sample_table(C, 450)
#S.to_csv(r'/datasets/buy_sell/S.csv',index=False)

# Did some labeling magic offline here
G = em.read_csv_metadata('/datasets/buy_sell/G_sampled.csv', 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_id', fk_rtable='rtable_id')
print('Length is ' + str(len(G)))


rf = em.RFMatcher(name='RF', random_state=0)


feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)

# Remove the id comparisons
feature_table = feature_table.drop([0, 1, 2, 3], axis=0)

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
CLF = {"RandomForest":rf}
for clf_name in CLF:
  for strategy_name in strategies:
    clf = CLF[clf_name]
    batch_size = 4
    rounds = 5
    F = Features
    while True:
        anno_batch = RS(Features,batch_size)    # 第一批标注样本只能随机选取
        if sum(Features['gold'][anno_batch]) > 0:
            break
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


##### Evaluate on the ENTIRE dataset #####
G = em.read_csv_metadata('/datasets/buy_sell/abtbuy_goldstandard.csv', 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_id', fk_rtable='rtable_id')
Features = em.extract_feature_vecs(G, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)




H = em.extract_feature_vecs(G, 
                            feature_table=feature_table, 
                            attrs_after='gold',
                            show_progress=False)

predictions = clf.predict(table=Features, exclude_attrs=['_id', 'ltable_id','rtable_id', 'gold'], append=True, target_attr='predicted', inplace=False)

eval_result = em.eval_matches(predictions, 'gold', 'predicted')
em.print_eval_summary(eval_result)


############################## Magellan with RF ###############################
############################## Magellan with RF ###############################
############################## Magellan with RF ###############################
############################## Magellan with RF ###############################
IJ = em.split_train_test(G, train_proportion=0.001, random_state=0)
I = IJ['train']
J = IJ['test']



result = em.select_matcher([rf], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
        k=5,
        target_attr='gold', metric_to_select_matcher='precision', random_state=0)
result['cv_stats']
result = em.select_matcher([rf], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
        k=5,
        target_attr='gold', metric_to_select_matcher='recall', random_state=0)
result['cv_stats']

L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)

rf.fit(table=H, 
       exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
       target_attr='gold')

predictions = rf.predict(table=L, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
              append=True, target_attr='predicted', inplace=False)
eval_result = em.eval_matches(predictions, 'gold', 'predicted')
em.print_eval_summary(eval_result)
############################## Magellan with RF ###############################
############################## Magellan with RF ###############################
############################## Magellan with RF ###############################
############################## Magellan with RF ###############################


