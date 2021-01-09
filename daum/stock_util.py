import pandas as pd
from pykrx.website.krx.market.core import MKD30030

market = {"ALL"   : "", 
          "KOSPI" : "1001", 
          "KOSDAQ": "2001", 
          "KONEX" : "N001"}

#local 에 받아놔서 중복으로 안 요청하게 하기


stock_df = None
def get_stock_info_list():
    
    global stock_df

    if stock_df is None:
        kospi_df = MKD30030().fetch('20210108', market.get("KOSPI"), 'ST', 0)
        kosdaq_df = MKD30030().fetch('20210108', market.get("KOSDAQ"), 'ST', 0)
        # 병합
        # https://www.geeksforgeeks.org/python-pandas-dataframe-append/
        stock_df = kospi_df.append(kosdaq_df, ignore_index=True)

    return stock_df

def get_stock_name(ticker_code):
    return
    