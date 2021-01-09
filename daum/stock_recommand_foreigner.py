
# 참고
# https://velog.io/@shchoice/Ajax-%EC%A0%81%EC%9A%A9%EB%90%9C-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-%EC%8A%A4%ED%81%AC%EB%9E%98%EC%9D%B4%ED%95%91Daum-%EC%A3%BC%EC%8B%9D
# http://pythonstudy.xyz/python/article/511-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%BD%94%EB%94%A9-%EC%8A%A4%ED%83%80%EC%9D%BC

import json
import pandas as pd

from fake_useragent import UserAgent
from urllib.request import urlopen, Request


from stock_util import get_stock_info_list




class RecommandStockByForeigner:

    def __init__(self, ticker_code, score, data, total_volumn):
        self.score = score
        self.ticker_code = ticker_code
        self.data = data
        self.total_volumn = total_volumn

#singletone pattern으로 만들기
class StockRecommnaderByForeigner:

    #1. 외국인 / 기관 매매 table 가져오기
    def __init__(self):
        print("get fake user agent")
        self.user_agent = UserAgent()
        self.all_daily_stock_result = [] # or use DB
        pass


    def get_daily_stock_result(self, ticker_code):


        #daum parsing
        #https://velog.io/@shchoice/Ajax-%EC%A0%81%EC%9A%A9%EB%90%9C-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-%EC%8A%A4%ED%81%AC%EB%9E%98%EC%9D%B4%ED%95%91Daum-%EC%A3%BC%EC%8B%9D

        if type(ticker_code) is int:
            ticker_code = 'A' + format(ticker_code, '06d')
        elif type(ticker_code) is str:
            #check 'A'+6 number
            pass
        else:
            raise TypeError("ticker_code must be int or string that prefix is 'A' or 'a' ")

        #days?symbolCode=A005930&page=1&perPage=50
        url = 'https://finance.daum.net/api/charts/investors/days?symbolCode={}&page=1&perPage=50'.format(ticker_code)
        headers = {
            'referer'    : 'https://finance.daum.net/chart/{}/investors'.format(ticker_code),
            'User-Agent' : self.user_agent.chrome
        }
        response = urlopen(Request(url, headers = headers)).read().decode('utf-8')
        stock_result_json = json.loads(response)
        stock_result_json["ticker_code"] = ticker_code[1:]
        return stock_result_json

    def get_all_daily_stock_result(self):
        
        print("start to get all daily stock result")
        if not self.all_daily_stock_result:

            #1. 병렬처리
            ticker_code_list = get_stock_info_list()['종목코드']
            for ticker_code in ticker_code_list:
                self.all_daily_stock_result.append( self.get_daily_stock_result('A'+ticker_code))
                
        print("end to get all daily stock result")
        return self.all_daily_stock_result

    def get_recommand_stock_list(self):

        #뭔가 이상함... 좀더 낫게 바꾸자
        self.get_all_daily_stock_result()

        #병렬처리
        recommand_stock_list = []
        for stock_json in self.all_daily_stock_result:
            score = 0
            index = -1
            temp_foreigner_trade_history_info = []
            total_volumn = 0
            print("get score of", stock_json["ticker_code"])
            for foreigner_trade_history in reversed(stock_json["data"]):
                if index < -5:
                    break
                foreigner_volumn = foreigner_trade_history["foreignStraightPurchaseVolume"]
                
                if foreigner_volumn > 0:
                    score += (6+index)

                total_volumn += foreigner_volumn
                temp_foreigner_trade_history_info.append(foreigner_volumn)
                index -= 1

            if score >= 9:
                recommand_stock_list.append( 
                    RecommandStockByForeigner(stock_json["ticker_code"], 
                                              score, 
                                              temp_foreigner_trade_history_info,
                                              total_volumn)
                )

        return recommand_stock_list

                

if __name__ == "__main__":

    s = StockRecommnaderByForeigner()
    #j = s.get_daily_stock_result(95570)
    #print(j)
    result =  s.get_recommand_stock_list()
    
    #multiple sort : https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
    result.sort(key=lambda x: (x.score, x.total_volumn))

    for stock_info in result:
        print(stock_info.score, 
              stock_info.ticker_code, 
              get_stock_info_list().loc[get_stock_info_list()['종목코드'] == stock_info.ticker_code, '종목명'].iloc[0],
              stock_info.total_volumn,
              stock_info.data)


    #print(ticker[100]['foreignStraightPurchaseVolume'])



    

        
        

