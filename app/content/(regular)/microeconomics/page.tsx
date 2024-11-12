"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { LineChart } from "@mui/x-charts/LineChart";
import {
  NEXT_PUBLIC_CPI,
  NEXT_PUBLIC_REAL_GDP,
  NEXT_PUBLIC_INFLATION,
  NEXT_PUBLIC_RETAIL_SALES,
  NEXT_PUBLIC_INTEREST_RATES,
  NEXT_PUBLIC_UNEMPLOYMENT_RATE,
  NEXT_PUBLIC_CPI_DATE,
  NEXT_PUBLIC_RETAIL_SALES_DATE,
  NEXT_PUBLIC_INFLATION_DATE,
  NEXT_PUBLIC_REAL_GDP_DATE,
  NEXT_PUBLIC_INTEREST_RATES_DATE,
  NEXT_PUBLIC_UNEMPLOYMENT_RATE_DATE,
} from "@/app/constants/api_properties";
import LineChartCard from "@/app/components/LineChartComponent";

export default function Overview() {
  const searchParams = useSearchParams();
  const input = searchParams.get("company");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const [chartData, setChartData] = useState({
    cpi: [],
    retail_sales: [],
    inflation: [],
    real_gdp: [],
    interest_rates: [],
    unemployment_rate: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/micro?company=AAPL`
        );
        const responseData = await response.json();

        if (!response.ok) {
          setError(
            `Error: ${
              responseData.error || "An unexpected error occurred"
            } for input "${input}"`
          );
          setLoading(false);
          return;
        }

        // Extract dates and data arrays for each chart type
        const cpiDatesArray = responseData[NEXT_PUBLIC_CPI_DATE] || [];
        const retailSalesDatesArray =
          responseData[NEXT_PUBLIC_RETAIL_SALES_DATE] || [];
        const inflationDatesArray =
          responseData[NEXT_PUBLIC_INFLATION_DATE] || [];
        const realGdpDatesArray = responseData[NEXT_PUBLIC_REAL_GDP_DATE] || [];
        const interestRatesDatesArray =
          responseData[NEXT_PUBLIC_INTEREST_RATES_DATE] || [];
        const unemploymentRateDatesArray =
          responseData[NEXT_PUBLIC_UNEMPLOYMENT_RATE_DATE] || [];

        const cpiArray = responseData[NEXT_PUBLIC_CPI] || [];
        const retailSalesArray = responseData[NEXT_PUBLIC_RETAIL_SALES] || [];
        const inflationArray = responseData[NEXT_PUBLIC_INFLATION] || [];
        const realGdpArray = responseData[NEXT_PUBLIC_REAL_GDP] || [];
        const interestRatesArray =
          responseData[NEXT_PUBLIC_INTEREST_RATES] || [];
        const unemploymentRateArray =
          responseData[NEXT_PUBLIC_UNEMPLOYMENT_RATE] || [];

        // Create chart data for each metric
        setChartData({
          cpi: cpiDatesArray.map((date, index) => ({
            date,
            cpi: parseFloat(cpiArray[index]) || 0,
          })),
          retail_sales: retailSalesDatesArray.map((date, index) => ({
            date,
            retail_sales: parseFloat(retailSalesArray[index]) || 0,
          })),
          inflation: inflationDatesArray.map((date, index) => ({
            date,
            inflation: parseFloat(inflationArray[index]) || 0,
          })),
          real_gdp: realGdpDatesArray.map((date, index) => ({
            date,
            real_gdp: parseFloat(realGdpArray[index]) || 0,
          })),
          interest_rates: interestRatesDatesArray.map((date, index) => ({
            date,
            interest_rates: parseFloat(interestRatesArray[index]) || 0,
          })),
          unemployment_rate: unemploymentRateDatesArray.map((date, index) => ({
            date,
            unemployment_rate: parseFloat(unemploymentRateArray[index]) || 0,
          })),
        });

        setLoading(false);
        setError(null);
      } catch (error) {
        console.error("Error getting data:", error);
        setError("Failed to fetch data");
        setLoading(false);
      }
    };

    if (input) {
      fetchData();
    } else {
      setLoading(false);
    }
  }, [input]);

  return (
    <div className="container-fluid h-100 d-flex flex-column gap-3 pb-5">
      {error ? (
        <div style={{ color: "red", textAlign: "center", fontWeight: "bold" }}>
          {error}
        </div>
      ) : (
        <>
          {loading ? (
            <div className="d-flex align-items-center justify-content-center w-100 h-100">
              <div
                className="spinner-border text-primary"
                style={{ width: 100, height: 100 }}
              ></div>
            </div>
          ) : (
            <>
              {/* Render each chart */}

              <LineChartCard
                title="CPI"
                dataToDisplay={[...chartData.cpi].reverse()}
                xKey="date"
                yKey="cpi"
              />

              <LineChartCard
                title="Retail Sales"
                dataToDisplay={[...chartData.retail_sales].reverse()}
                xKey="date"
                yKey="retail_sales"
              />

              <LineChartCard
                title="Inflation"
                dataToDisplay={[...chartData.inflation].reverse()}
                xKey="date"
                yKey="inflation"
              />

              <LineChartCard
                title="Real GDP"
                dataToDisplay={[...chartData.real_gdp].reverse()}
                xKey="date"
                yKey="real_gdp"
              />

              <LineChartCard
                title="Interest Rates"
                dataToDisplay={[...chartData.interest_rates].reverse()}
                xKey="date"
                yKey="interest_rates"
              />

              <LineChartCard
                title="Unemployment Rate"
                dataToDisplay={[...chartData.unemployment_rate].reverse()}
                xKey="date"
                yKey="unemployment_rate"
              />
            </>
          )}
        </>
      )}
    </div>
  );
}
