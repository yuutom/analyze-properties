from retry import retry
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
# util
from util.common_util import common_util_class
from util.csv_and_pd_util import csv_and_pd_util_class
from util.ai_util import ai_util_class


comonn_util = common_util_class()
csv_and_pd_util = csv_and_pd_util_class()
ai_util = ai_util_class()


# スクレイピング実行 → result.csv作成
# comonn_util.scraping()


# 前処理実行 → preprocessed_result.csv作成
# comonn_util.preprocess()


# ランダムフォレストのAIモデル作成
# model, X = ai_util.create_model()


# 家賃を予測し、Seriesオブジェクトで取得
# pred_series = ai_util.predict_rent(model, X)


# 'preprocessed_result.csv'のDataFrameと予測家賃のSeriesを連結
# df = pd.read_csv('preprocessed_result.csv')
# df_concat = pd.concat([df, pred_series], axis=1)


# 連結したDataFrameをcsv出力
# csv_and_pd_util.to_csv(df_concat, "all_result.csv")


# all_result.csvにスコア(家賃-予測家賃)カラムを追加
# df = pd.read_csv('all_result.csv')
# df["スコア"] = df["家賃"] - df["予測家賃"]
# csv_and_pd_util.to_csv(df, "all_result.csv")


# all_result.csvをスコアでソートしたDataFrameをcsv出力
# df.sort_values(by="スコア", inplace=True, ascending=True)
# csv_and_pd_util.to_csv(df, "score.csv")

