#!-*- coding:utf8 -*-
ini_path='../ini_data/' #原始数据的存储路径
interim_path='../interim_data/' # 中间数据的存储路径
result_path='../result/' #结果数据的存储路径


ini_CS_path='../ini_data/ini_chairman_statement/'  # 原始chairman statement 的路径
filtered_CS_path='../interim_data/target_chairman_statement/'   # 处理后的chairman statement 的路径
CS_word_dict_path='../interim_data/CS_word_dict/'  #将chairman statement处理成词-词频的字典后的存储路径

ini_WG_path='../ini_data/ini_wordgroup/' # 原始的word group的存储路径
list_WG_path='../interim_data/wordgroup_list/'  # 整理后的word group 的存储路径

doc_length_path='../interim_data/docLength_all.txt'  #所有处理后的chairman statement的长度

# word vector
word_vector_root='../interim_data/word_vector/' # 存储词向量的根目录
one_hot_word_vector_dict_path='../interim_data/word_vector/onehot_word_vector/'  # one hot 形式的词向量
bow_word_vector_dict_path='../interim_data/word_vector/bow_word_vector/'  # bag of word 形式的词向量
bow_delta_tone_dict_path='../interim_data/word_vector/bow_delta_tone/' #使用bag of word形式词向量计算的delta tone
bow_word_vector_suffix='_bow_vector_dict.txt'

# 统计数据
Fre_count_dict_path='../interim_data/experimental_1_Effectiveness/senti_word_freq.txt'
a='result/ab_positive_words_differ.txt'
b='result/ab_negative_words_differ.txt'

c='result/ab_differ_senti_words_count.csv'
d='result/differ_senti_words_count.xls'





