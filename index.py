import pandas as pd
import csv
from util.common_util import common_util_class
from util.csv_and_pd_util import csv_and_pd_util_class
from util.ai_util import ai_util_class


comonn_util = common_util_class()
csv_and_pd_util = csv_and_pd_util_class()
ai_util = ai_util_class()

df = pd.read_csv('score.csv')