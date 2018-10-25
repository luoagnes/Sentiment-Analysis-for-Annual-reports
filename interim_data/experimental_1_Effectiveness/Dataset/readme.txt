dataset是一个list，list中每一个元素是一个样本，由27维构成，最后一维为类标。前面26维为输入向量，构成如下：
1) 公司类型：12维， 前面2维为AB类型，后面10维表示大的类别，该部分采用onehot编码
2）金融指数数据：11维，是计算delta value之后再归一化得到的结果，
                 对应的指数依次为："ROE_Diluted","BPS", "EPS","Equity_Multiplier", "Book_Value","Market_capitalization","PE_Ratio","Size", "Turnover", "Votility", "BM"

3）情感delta tone：3维，分别是用Schmeling, Kang&Feldman, Tetlock 方法，并采用negative情感词和global全局词频计算的tone，然后去delta value，最后再归一化得到的值。
该数据集总共包含1706个样本。
