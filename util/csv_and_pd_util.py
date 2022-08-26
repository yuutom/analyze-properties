import pandas as pd
import csv
import re
from const.data_const import data_const_class


class csv_and_pd_util_class:
    
    def csv_drop_duplicates(self, df):
        """
        csvの重複を削除したDataFrameを取得

        Args:
            df (Dataframe): 重複を削除したいDataFrameオブジェクト
        """
        # "URL", "アクセス"をキーに重複データを削除
        df.drop_duplicates(subset=["URL", "アクセス"], inplace=True)

        # "アドレス", "カテゴリー", "名称", "家賃", "敷金", "構造", "礼金", "管理費", "築年数", "間取り", "階数", "面積", "沿線", "駅", "徒歩"をキーに重複データを削除
        df.drop_duplicates(subset=["アドレス", "カテゴリー", "名称", "家賃", "敷金", "構造", "礼金", "管理費", "築年数", "間取り", "階数", "面積", "沿線", "駅", "徒歩"], inplace=True)
        
        return df

    def to_csv(self, df: object, file_name: str):
        """
        DataFrameをcsvで保存

        Args:
            df (Dataframe): csvに変換したいDataFrameオブジェクト
            file_name (str): csvのファイル名
        """
        # csvで保存
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        
        
    def shape_access_column(self, df):
        """
        「アクセス」カラムを整形する
        ・「アクセス」から「沿線」「駅」「徒歩」を抽出（さらに「徒歩」は数値データに変換）
        ・「アクセス」が駅でないデータ（バスとか）は除外
        ・徒歩圏内でないでデータ（車で3分とか）は除外
        Args:
            df (Dataframe): DataFrameオブジェクト

        Returns:
            object: 「アクセス」カラムを整形したDataFrame
        """
        # アクセスがNullの行を排除
        df = df[df["アクセス"].isnull()==False]
        
        # 沿線を抽出
        df["沿線"] = df["アクセス"].apply(lambda x: x.split("/")[0])
        
        # 沿線に線が入ってる行のみを抽出 *バスとかを排除
        df = df[df["沿線"].str.contains("線")]
        
        # アクセスから駅を抽出
        df["駅"] = df["アクセス"].apply(lambda x: x.split(" ")[0].split("/")[1])
        
        # 徒歩圏内でない物件を排除
        df = df[df["アクセス"].str.contains("歩")]
        
        # アクセスから徒歩を抽出
        df["徒歩"] = df["アクセス"].apply(lambda x: int(re.findall(r"[0-9]+", x.split(" ")[1])[0]))
        
        return df
    
    def shape_address_column(self, df):
        """
        「アドレス」カラムを整形する

        Args:
            df (Dataframe): DataFrameオブジェクト

        Returns:
            object: 「アドレス」カラムを整形したDataFrame
        """

        df["区"] = df["アドレス"].apply(lambda x: re.findall(r"東京都(.*区)", x)[0])
        
        return df
    
    def remove_outliers(self, df):
        """
        外れ値を除去

        Args:
            df (DataFrame): _description_

        Returns:
            _type_: _description_
        """
        std = df.describe().at["std", "家賃"]
        mean = df.describe().at["mean", "家賃"]
        print("家賃の標準偏差: {}".fortmat(std))
        print("家賃の平均: {}".format(mean))
        df = df[df["家賃"] >= mean-3*std]
        df = df[df["家賃"] <= mean+3*std]
        return df
    
    def get_train_and_test_data(self):
        pre_X = []
        pre_y = []
        with open('preprocessed_result.csv', 'rt') as f:
            dict_reader  = csv.DictReader(f)
            data = [row for row in dict_reader ]
            
        for row in data:
            age = row["築年数"]
            number_of_floors = 1 if len(re.findall(r"[0-9]+", row['階数'])) == 0 else int(re.findall(r"[0-9]+", row['階数'])[0])
            floor_plan = row["間取り"]
            railway_line = row["沿線"]
            station = row["駅"]
            foot = row['徒歩']
            district = row["区"]
            temp = [age, number_of_floors, floor_plan, railway_line, station, foot, district]
            pre_X.append(temp)
            pre_y.append(row['家賃'])
            
        X = pd.DataFrame(pre_X, columns=["築年数", "階数", "間取り", "沿線", "駅", "徒歩", "区"])
        y = pd.DataFrame(pre_y, columns=["家賃"])
        X = pd.get_dummies(X, columns=["間取り", "沿線", "駅", "区"])

        return X, y