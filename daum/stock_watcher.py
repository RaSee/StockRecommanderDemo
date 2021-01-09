#
# 참고
# https://velog.io/@shchoice/Ajax-%EC%A0%81%EC%9A%A9%EB%90%9C-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-%EC%8A%A4%ED%81%AC%EB%9E%98%EC%9D%B4%ED%95%91Daum-%EC%A3%BC%EC%8B%9D
# http://pythonstudy.xyz/python/article/511-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%BD%94%EB%94%A9-%EC%8A%A4%ED%83%80%EC%9D%BC

from stock_result_parser import StockDailyResult



        

if __name__ == "__main__":

    s = StockDailyResult()
    j = s.get_daily_stock_result(5930)
    ticker = s.get_ticker_code_list()



    

        
        

