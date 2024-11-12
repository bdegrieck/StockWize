from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_restful import Api, Resource

from BackEnd.Comparison.ticker_comparison import TickerComparison
from BackEnd.Data.data import CompanyData, MicroData
from BackEnd.constants import Finance, MicroEconomic
from BackEnd.validation import validate_ticker, TickerError
from BackEnd.Eda.eda import Eda
from BackEnd.Metadata.metadata import StockWizeMetadata

app = Flask(__name__)
CORS(app)
api = Api(app)

# TODO handle AAOL
class Overview(Resource):
    def get(self):
        symbol = request.args.get('company')
        try:
            ticker = validate_ticker(symbol=symbol)
            instance = CompanyData(ticker=ticker)
            overview = instance.overview
            time_series = instance.time_series

            if len(time_series) > 700:
                time_series = time_series.iloc[0: 700]

            data = {
                Finance.year_high: overview[Finance.year_high][0],
                Finance.year_low: overview[Finance.year_low][0],
                Finance.market_cap: overview[Finance.market_cap][0],
                Finance.description: overview[Finance.description][0],
                Finance.date: time_series[Finance.date].to_list(),
                Finance.close: time_series[Finance.close].to_list()
            }

            return jsonify(data)

        except TickerError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

class EDA(Resource):
    def get(self):
        symbol = request.args.get('company')
        try:
            ticker = validate_ticker(symbol=symbol)
            company_instance = CompanyData(ticker=ticker)
            time_series = company_instance.time_series
            eda_instance = Eda(ticker=ticker, time_series_data=time_series)
            data = eda_instance.mstl(value_column=Finance.close)
            for key, values in data.items():
                if len(values) > 1000:
                    values = values.iloc[0: 1000]
                data[key] = values.to_list()
            data[Finance.symbol] = ticker
            return jsonify(data)

        except TickerError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500


class Micro(Resource):
    def get(self):
        try:
            micro_instance = MicroData()
            data = {
                MicroEconomic.cpi_date: micro_instance.cpi[Finance.date].to_list(),
                MicroEconomic.cpi: micro_instance.cpi[MicroEconomic.cpi].to_list(),
                MicroEconomic.real_gdp: micro_instance.real_gdp[MicroEconomic.real_gdp].to_list(),
                MicroEconomic.real_gdp_date: micro_instance.real_gdp[Finance.date].to_list(),
                MicroEconomic.inflation: micro_instance.inflation[MicroEconomic.inflation].to_list(),
                MicroEconomic.inflation_date: micro_instance.inflation[Finance.date].to_list(),
                MicroEconomic.retail_sales: micro_instance.retail_sales[MicroEconomic.retail_sales].to_list(),
                MicroEconomic.retail_sales_date: micro_instance.retail_sales[Finance.date].to_list(),
                MicroEconomic.interest_rates: micro_instance.federal_funds_rate[MicroEconomic.interest_rates].to_list(),
                MicroEconomic.interest_rates_date: micro_instance.federal_funds_rate[Finance.date].to_list(),
                MicroEconomic.unemployment_rate: micro_instance.unemployment_rate[MicroEconomic.unemployment_rate].to_list(),
                MicroEconomic.unemployment_rate_date: micro_instance.unemployment_rate[Finance.date].to_list()
            }
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500
        
class Metadata(Resource):
    def get(self):
        try:
            metadata = StockWizeMetadata()
            data = {
                "fun_fact" : metadata.fun_fact(),
                "last_updated" : metadata.get_last_weekday()
            }

            print(data)

            return jsonify(data)
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500


class Comparison(Resource):
    def get(self):
        try:
            input_1 = request.args.get('ticker1')
            input_2 = request.args.get('ticker2')
            ticker_1 = validate_ticker(symbol=input_1)
            ticker_2 = validate_ticker(symbol=input_2)

            # comparison info
            comp_instance = TickerComparison(ticker1=ticker_1, ticker2=ticker_2)
            comp = comp_instance.get_difference
            ticker_1_raw_data = comp_instance.get_ticker1_metadata
            ticker_2_raw_data = comp_instance.get_ticker2_metadata

            # handle unequal lengths
            ticker_1_len = len(ticker_1_raw_data.time_series)
            ticker_2_len = len(ticker_2_raw_data.time_series)
            if ticker_1_len > 700 and ticker_2_len > 700:
                ticker_1_raw_data.time_series = ticker_1_raw_data.time_series.iloc[0: 700]
                ticker_2_raw_data.time_series = ticker_2_raw_data.time_series.iloc[0: 700]
            else:
                if ticker_1_len > ticker_2_len:
                    ticker_1_raw_data.time_series = ticker_1_raw_data.time_series.iloc[:ticker_2_len]
                elif ticker_2_len > ticker_1_len:
                    ticker_2_raw_data.time_series = ticker_2_raw_data.time_series.iloc[:ticker_1_len]

            ticker_1_data = {
                Finance.symbol: ticker_1_raw_data.symbol,
                Finance.market_cap: ticker_1_raw_data.market_cap,
                Finance.reported_eps: ticker_1_raw_data.reported_eps,
                Finance.total_revenue: ticker_1_raw_data.total_revenue,
                Finance.profit: ticker_1_raw_data.profit,
                Finance.PPE: ticker_1_raw_data.ppe,
                Finance.date: ticker_1_raw_data.time_series[Finance.date].to_list(),
                Finance.close: ticker_1_raw_data.time_series[Finance.close].to_list()
            }

            ticker_2_data = {
                Finance.symbol: ticker_2_raw_data.symbol,
                Finance.market_cap: ticker_2_raw_data.market_cap,
                Finance.reported_eps: ticker_2_raw_data.reported_eps,
                Finance.total_revenue: ticker_2_raw_data.total_revenue,
                Finance.profit: ticker_2_raw_data.profit,
                Finance.PPE: ticker_2_raw_data.ppe,
                Finance.date: ticker_2_raw_data.time_series[Finance.date].to_list(),
                Finance.close: ticker_2_raw_data.time_series[Finance.close].to_list()
            }

            data = {
                Finance.ticker_1_data: ticker_1_data,
                Finance.ticker_2_data: ticker_2_data,
                Finance.comparison: comp
            }

            return jsonify(data)
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

class News(Resource):
    def get(self):
        try:
            symbol = request.args.get('company')
            ticker = validate_ticker(symbol=symbol)
            company_instance = CompanyData(ticker=ticker)
            news = company_instance.news
            return jsonify(news)
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500


class Test(Resource):
    def get(self):
        return jsonify({"Test": "Test Success"})

# Add resources to the API
api.add_resource(Overview, '/api/overview')
api.add_resource(EDA, '/api/eda')
api.add_resource(Test, '/api/test')
api.add_resource(Micro, '/api/micro')
api.add_resource(Metadata, '/api/metadata')
api.add_resource(Comparison, '/api/comparison')
api.add_resource(News, '/api/news')

if __name__ == "__main__":
    app.run(debug=True)
