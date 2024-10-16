from BackEnd.Data.data import CompanyData, MicroData, TechIndData


class TestCompanyData:

    def test_company_data(self):
        ticker = "AAPL"
        instance = CompanyData(ticker=ticker)

        time_series = instance.time_series
        earnings = instance.earnings
        overview = instance.overview
        income_statement = instance.income_statement
        cashflow = instance.cash_flow

        assert not time_series.empty
        assert not earnings.empty
        assert not overview.empty
        assert not income_statement.empty
        assert not cashflow.empty

    def test_tech_indicators(self):
        ticker = "AAPL"
        instance = TechIndData(ticker=ticker)

        sma = instance.sma
        ema = instance.ema
        rsi = instance.rsi
        bbands = instance.bbands
        adx = instance.adx

        assert not sma.empty
        assert not ema.empty
        assert not rsi.empty
        assert not bbands.empty
        assert not adx.empty

class TestMicroData:

    def test_micro_data(self):
        instance = MicroData()

        real_gdp = instance.real_gdp
        cpi = instance.cpi
        inflation = instance.inflation
        interest_rates = instance.federal_funds_rate
        retail_sales = instance.retail_sales
        unemployment_rate = instance.unemployment_rate

        assert not real_gdp.empty
        assert not cpi.empty
        assert not inflation.empty
        assert not interest_rates.empty
        assert not retail_sales.empty
        assert not unemployment_rate.empty
