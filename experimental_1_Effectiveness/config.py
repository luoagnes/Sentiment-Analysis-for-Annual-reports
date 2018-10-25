#-*- coding:utf8 -*-
input_root_path='../interim_data/experimental_1_Effectiveness/'
ini_fre_dict_path='../interim_data/experimental_1_Effectiveness/senti_word_freq.txt'
tone_dict_path='../interim_data/experimental_1_Effectiveness/tone_dict.txt'
delta_tone_dict_path='../interim_data/experimental_1_Effectiveness/delta_tone_dict.txt'

ALL_stock_list_path='../interim_data/stock_list/AB_stock_list.json'
MPE_stock_list_path='../interim_data/stock_list/MPE_stock_list.json'
OEE_stock_list_path='../interim_data/stock_list/OEE_stock_list.json'

type_code_dict_path='../interim_data/stock_type/AB_stock_type_code.json'
fin_dict_path='../interim_data/financial_index/all_financial_norm_delta_tone_pairs.txt'
gradient_dict_path='../interim_data/stock_price/AB_gradients.txt'
experiment_1_dataset_path='../interim_data/experimental_1_Effectiveness/experimental_1_dataset.txt'

X_l1=['neg', 'pos']
X_l2=['global', 'total']
X_tone=['','1', '2', '3', ['1', '2'], ['1', '3'], ['2', '3'], ['1', '2', '3']]

X_type=['type', ''] # ['X_type.txt', '']
X_financial=['Fin', '']
# financial_index_list=["ROE_Diluted", "BPS", "EPS","Equity_Multiplier", "Book_Value","Market_capitalization","PE_Ratio", "Size", "Turnover", "Votility", "BM"]


Y_path_list=['10', '120', '180', '20', '250', '30', '3', '5', '60', '7', '90', 'gradient']

X_root=['MPE', 'OEE', 'ALL']
root='../result/'

result_directory='result/'

years_flag_path='stock_years_flag.txt'

type_flag_path='../data/label_name.txt'
type_flag_name=['AB_type', 'Industry_type']

result_root='result/experimental_1/'

