from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource

from BackEnd.Data.data import CompanyData
from BackEnd.constants import Finance
from BackEnd.validation import validate_ticker

app = Flask(__name__)
CORS(app)
api = Api(app)


class TimeSeries(Resource):

    def get(self):
        symbol = request.args.get('company')
        ticker = validate_ticker(symbol=symbol)
        instance = CompanyData(ticker=ticker)
        overview = instance.overview
        time_series = instance.time_series.sort_values(by=Finance.date)

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

api.add_resource(TimeSeries, '/api/stock')

if __name__ == "__main__":
    app.run(debug=True)
