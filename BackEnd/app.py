from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_restful import Api, Resource

from BackEnd.Data.data import CompanyData
from BackEnd.constants import Finance
from BackEnd.validation import validate_ticker, TickerError
from BackEnd.Eda.eda import Eda

app = Flask(__name__)
CORS(app)
api = Api(app)


class Overview(Resource):
    def get(self):
        symbol = request.args.get('company')
        try:
            ticker = validate_ticker(symbol=symbol)
            instance = CompanyData(ticker=ticker)
            overview = instance.overview
            time_series = instance.time_series.sort_values(by=Finance.date, ascending=True)

            if len(time_series) > 700:
                time_series = time_series.iloc[-700:]

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
            return jsonify(data)

        except TickerError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

class Test(Resource):
    def get(self):
        return jsonify({"Test": "Test Success"})

# Add resources to the API
api.add_resource(Overview, '/api/overview')
api.add_resource(EDA, '/api/eda')
api.add_resource(Test, '/api/test')

if __name__ == "__main__":
    app.run(debug=True)
