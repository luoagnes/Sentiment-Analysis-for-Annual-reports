#!-*- coding:utf8 -*-

stock_price_path='../interim_data/stock_price/Close_Price.json'
stock_volume_path='../interim_data/stock_price/Volume.json'
actual_return_path='../interim_data/stock_price/Actual_return.json'
annual_report_published_date_path='../interim_data/annual_reports_published_date/AB_stocks_published_date_dict.txt'

ini_ROE_Diluted_path='../ini_data/ini_financial_index_data/ROE Diluted (HK).xlsx'  # 原始的ROE_Diluted的路径
ROE_Diluted_dict_path='../interim_data/financial_index/financial_index_dict/ROE_Diluted.json'  # 处理后的dict形式的ROE_Diluted的路径
normalize_ROE_Diluted_dict_path='../interim_data/financial_index/Normalize_financial_index/ROE_Diluted.json'  # 处理后并归一化的dict形式的ROE_Diluted的路径
delta_ROE_Diluted_dict_path='../interim_data/financial_index/delta_financial_index_dict/ROE_Diluted.json'  # 处理后的dict形式的delta ROE_Diluted的路径
norm_delta_ROE_Diluted_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/ROE_Diluted.json'

ini_BPS_path='../ini_data/ini_financial_index_data/BPS (HK).xlsx'  # 原始的BPS的路径
BPS_dict_path='../interim_data/financial_index/financial_index_dict/BPS.json'  # 处理后的dict形式的BPS的路径
normalize_BPS_dict_path='../interim_data/financial_index/Normalize_financial_index/BPS.json'  # 处理后并归一化的dict形式的BPS的路径
delta_BPS_dict_path='../interim_data/financial_index/delta_financial_index_dict/BPS.json'  # 处理后的dict形式的delta BPS的路径
norm_delta_BPS_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/BPS.json'

ini_Outstanding_path='../ini_data/ini_financial_index_data/Outstanding 2 (HK)(1).xlsx'  # 原始的Outstanding的路径
Outstanding_dict_path='../interim_data/financial_index/financial_index_dict/Outstanding.json'  # 处理后的dict形式的Outstanding的路径
normalize_Outstanding_dict_path='../interim_data/financial_index/Normalize_financial_index/Outstanding.json'  # 处理后并归一化的dict形式的Outstanding的路径
delta_Outstanding_dict_path='../interim_data/financial_index/delta_financial_index_dict/Outstanding.json'  # 处理后的dict形式的delta Outstanding的路径
norm_delta_Outstanding_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Outstanding.json'

ini_EPS_path='../ini_data/ini_financial_index_data/EPS Basic (HK).xlsx'  # 原始的EPS的路径
EPS_dict_path='../interim_data/financial_index/financial_index_dict/EPS.json'  # 处理后的dict形式的EPS的路径
normalize_EPS_dict_path='../interim_data/financial_index/Normalize_financial_index/EPS.json'  # 处理后并归一化的dict形式的EPS的路径
delta_EPS_dict_path='../interim_data/financial_index/delta_financial_index_dict/EPS.json'  # 处理后的dict形式的delta EPS的路径
norm_delta_EPS_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/EPS.json'

ini_Equity_Multiplier_path='../ini_data/ini_financial_index_data/Equity Multiplier (HK).xlsx'  # 原始的Equity_Multiplier的路径
Equity_Multiplier_dict_path='../interim_data/financial_index/financial_index_dict/Equity_Multiplier.json'  # 处理后的dict形式的Equity_Multiplier的路径
normalize_Equity_Multiplier_dict_path='../interim_data/financial_index/Normalize_financial_index/Equity_Multiplier.json'  # 处理后并归一化的dict形式的Equity_Multiplier的路径
delta_Equity_Multiplier_dict_path='../interim_data/financial_index/delta_financial_index_dict/Equity_Multiplier.json'  # 处理后的dict形式的delta Equity_Multiplier的路径
norm_delta_Equity_Multiplier_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Equity_Multiplier.json'

ini_Book_Value_path='../ini_data/ini_financial_index_data/Book Value (HK).xlsx'  # 原始的Book_Value的路径
Book_Value_dict_path='../interim_data/financial_index/financial_index_dict/Book_Value.json'  # 处理后的dict形式的Book_Value的路径
normalize_Book_Value_dict_path='../interim_data/financial_index/Normalize_financial_index/Book_Value.json'  # 处理后并归一化的dict形式的Book_Value的路径
delta_Book_Value_dict_path='../interim_data/financial_index/delta_financial_index_dict/Book_Value.json'  # 处理后的dict形式的delta Book_Value的路径
norm_delta_Book_Value_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Book_Value.json'

Market_capitalization_dict_path='../interim_data/financial_index/financial_index_dict/Market_capitalization.json'  # 处理后的dict形式的Market_capitalization的路径
normalize_Market_capitalization_dict_path='../interim_data/financial_index/Normalize_financial_index/Market_capitalization.json'  # 处理后并归一化的dict形式的Market_capitalization的路径
delta_Market_capitalization_dict_path='../interim_data/financial_index/delta_financial_index_dict/Market_capitalization.json'  # 处理后的dict形式的delta Market_capitalization的路径
norm_delta_Market_capitalization_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Market_capitalization.json'

PE_Ratio_dict_path='../interim_data/financial_index/financial_index_dict/PE_Ratio.json'  # 处理后的dict形式的PE_Ratio的路径
normalize_PE_Ratio_dict_path='../interim_data/financial_index/Normalize_financial_index/PE_Ratio.json'  # 处理后并归一化的dict形式的PE_Ratio的路径
delta_PE_Ratio_dict_path='../interim_data/financial_index/delta_financial_index_dict/PE_Ratio.json'  # 处理后的dict形式的delta PE_Ratio的路径
norm_delta_PE_Ratio_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/PE_Ratio.json'

Size_dict_path='../interim_data/financial_index/financial_index_dict/Size.json'  # 处理后的dict形式的Size的路径
normalize_Size_dict_path='../interim_data/financial_index/Normalize_financial_index/Size.json'  # 处理后并归一化的dict形式的Size的路径
delta_Size_dict_path='../interim_data/financial_index/delta_financial_index_dict/Size.json'  # 处理后的dict形式的delta Size的路径
norm_delta_Size_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Size.json'  # 处理后的dict形式的delta Size的路径

Turnover_dict_path='../interim_data/financial_index/financial_index_dict/Turnover.json'  # 处理后的dict形式的Turnover的路径
normalize_Turnover_dict_path='../interim_data/financial_index/Normalize_financial_index/Turnover.json'  # 处理后并归一化的dict形式的Turnover的路径
delta_Turnover_dict_path='../interim_data/financial_index/delta_financial_index_dict/Turnover.json'  # 处理后的dict形式的delta Turnover的路径
norm_delta_Turnover_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Turnover.json'

Votility_dict_path='../interim_data/financial_index/financial_index_dict/Votility.json'  # 处理后的dict形式的Votility的路径
normalize_Votility_dict_path='../interim_data/financial_index/Normalize_financial_index/Votility.json'  # 处理后并归一化的dict形式的Votility的路径
delta_Votility_dict_path='../interim_data/financial_index/delta_financial_index_dict/Votility.json'  # 处理后的dict形式的delta Votility的路径
norm_delta_Votility_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/Votility.json'

BM_dict_path='../interim_data/financial_index/financial_index_dict/BM.json'  # 处理后的dict形式的BM的路径
normalize_BM_dict_path='../interim_data/financial_index/Normalize_financial_index/BM.json'  # 处理后并归一化的dict形式的Votility的路径
delta_BM_dict_path='../interim_data/financial_index/delta_financial_index_dict/BM.json'  # 处理后的dict形式的delta BM的路径
norm_delta_BM_dict_path='../interim_data/financial_index/norm_delta_financial_index_dict/BM.json'

financial_error_list=['00823','08008','87001','02778','00778','00291','00363']
financial_index_list=["ROE_Diluted","BPS", "EPS","Equity_Multiplier", "Book_Value","Market_capitalization","PE_Ratio","Size", "Turnover", "Votility", "BM"]

count_delta_data_path='../interim_data/financial_index/all_financial_delta_tone'
count_data_path='../interim_data/financial_index/all_financial_tone'
all_financial_index_pair_path='../interim_data/financial_index/all_financial_norm_delta_tone_pairs'