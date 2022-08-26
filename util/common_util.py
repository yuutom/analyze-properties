from retry import retry
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

from const.system_const import system_const_class
from util.csv_and_pd_util import csv_and_pd_util_class


class common_util_class:
    def scraping(self):
        """
        スクレイピングを実行
        """
        system_const_class_object = system_const_class()
        csv_and_pd_util_class_object = csv_and_pd_util_class()
        
        all_data = []
        max_page = system_const_class_object.MAX_PAGE
        base_url = system_const_class_object.BASE_URL
        
        for page in range(1, max_page+1):
            # URLを定義
            url = base_url.format(page)
            
            # htmlデータ取得
            soup = self.get_html(url)
            
            # 全要素を抽出
            items = soup.findAll("div", {"class": "cassetteitem"})
            print("page", page, "items", len(items))
            
            # それぞれの要素を処理
            for item in items:
                stations = item.findAll("div", {"class": "cassetteitem_detail-text"})
                
                # 駅ごと 
                for station in stations:
                    base_data = {}
        
                    # ベース情報を取得   
                    base_data["名称"] = item.find("div", {"class": "cassetteitem_content-title"}).getText().strip()
                    base_data["カテゴリー"] = item.find("div", {"class": "cassetteitem_content-label"}).getText().strip()
                    base_data["アドレス"] = item.find("li", {"class": "cassetteitem_detail-col1"}).getText().strip()
                    base_data["アクセス"] = station.getText().strip()
                    base_data["築年数"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip()
                    base_data["構造"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[1].getText().strip()
                    
                    # 部屋ごと
                    tbodys = item.find("table", {"class": "cassetteitem_other"}).findAll("tbody")
                    
                    for tbody in tbodys:
                        data = base_data.copy()
        
                        data["階数"] = tbody.findAll("td")[2].getText().strip()
        
                        data["家賃"] = tbody.findAll("td")[3].findAll("li")[0].getText().strip()
                        data["管理費"] = tbody.findAll("td")[3].findAll("li")[1].getText().strip()
        
                        data["敷金"] = tbody.findAll("td")[4].findAll("li")[0].getText().strip()
                        data["礼金"] = tbody.findAll("td")[4].findAll("li")[1].getText().strip()
        
                        data["間取り"] = tbody.findAll("td")[5].findAll("li")[0].getText().strip()
                        data["面積"] = tbody.findAll("td")[5].findAll("li")[1].getText().strip()
                        
                        data["URL"] = "https://suumo.jp" + tbody.findAll("td")[8].find("a").get("href")
                        
                        all_data.append(data)    
        
        # Dataframeに変換
        df = pd.DataFrame(all_data)
        csv_and_pd_util_class_object.to_csv(df, 'result.csv')
        
        
    def preprocess(self):
        
        csv_and_pd_util_class_object = csv_and_pd_util_class()
        
        # csvデータ読み込み
        df = pd.read_csv('result.csv')
        
        # 各種データを数値データに変換
        df["家賃"] = df["家賃"].apply(self.get_number)
        df["管理費"] = df["管理費"].apply(self.get_number)
        df["管理費"] = df["管理費"] / 10000
        df["敷金"] = df["敷金"].apply(self.get_number)
        df["礼金"] = df["礼金"].apply(self.get_number)
        df["面積"] = df["面積"].apply(self.get_number)
        df["築年数"] = df["築年数"].apply(self.get_number)
        
        # 「アクセス」カラムを整形
        df = csv_and_pd_util_class_object.shape_access_column(df)
        
        # 「アドレス」カラムを整形
        df = csv_and_pd_util_class_object.shape_address_column(df)
        
        # 「重複」を削除
        df = csv_and_pd_util_class_object.csv_drop_duplicates(df)
        
        # 外れ値を除去
        df = csv_and_pd_util_class_object.remove_outliers(df)

        # csvで保存
        csv_and_pd_util_class_object.to_csv(df, 'preprocessed_result.csv')

        
    @retry(tries=3, delay=10, backoff=2)
    def get_html(self, url):
        """
        htmlを取得

        Args:
            url (str): スクレイピング対象のURL

        Returns:
            object: BeautifulSoupのオブジェクト
        """
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup
    
    
    def get_number(self, value):
        """
        文字列から数値を抽出（データ整形用）

        Args:
            value (str): 対象の文字列

        Returns:
            float: 文字列中の数値
        """
        n = re.findall(r"[0-9.]+", value)
        
        if len(n) != 0:
            return float(n[0])
        else:
            return 0
        
        
