#!/bin/python
# Invoke this script from /root

import sys
sys.path.append('/magellan/py_entitymatching/py_entitymatching/')


import py_entitymatching as em
import pandas as pd
import os


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


G = em.label_table(S, 'gold') # This step raises an error


path_G = em.get_install_path() + os.sep + 'datasets' + os.sep + 'end-to-end' + os.sep + 'restaurants/lbl_restnt_wf1.csv'
G = em.read_csv_metadata(path_G, 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_id', fk_rtable='rtable_id')
len(G)



IJ = em.split_train_test(G, train_proportion=0.7, random_state=0)
I = IJ['train']
J = IJ['test']


dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')


feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)
H = em.extract_feature_vecs(I, 
                            feature_table=feature_table, 
                            attrs_after='gold',
                            show_progress=False)



# One is precision, one is recall
result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
        k=5,
        target_attr='gold', metric_to_select_matcher='precision', random_state=0)
result['cv_stats']
result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
        k=5,
        target_attr='gold', metric_to_select_matcher='recall', random_state=0)
result['cv_stats']


L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)

dt.fit(table=H, 
       exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
       target_attr='gold')

predictions = dt.predict(table=L, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
              append=True, target_attr='predicted', inplace=False)

eval_result = em.eval_matches(predictions, 'gold', 'predicted')
em.print_eval_summary(eval_result)


