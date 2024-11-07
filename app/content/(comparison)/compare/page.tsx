"use client";

import { TextBox, TextBoxContainer } from "@/app/components/TextBox";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { LineChart } from "@mui/x-charts/LineChart";
import Skeleton from "@mui/material/Skeleton";
import {
  NEXT_PUBLIC_CLOSE,
  NEXT_PUBLIC_DATE,
  NEXT_PUBLIC_DESCRIPTION,
  NEXT_PUBLIC_DIVIDEND,
  NEXT_PUBLIC_MARKET_CAP,
  NEXT_PUBLIC_NAME,
  NEXT_PUBLIC_REPORTED_EPS,
  NEXT_PUBLIC_SYMBOL,
  NEXT_PUBLIC_YEAR_HIGH,
  NEXT_PUBLIC_TOTAL_REVENUE,
  NEXT_PUBLIC_PROFIT,
  NEXT_PUBLIC_PPE,
  COMPARISON
} from "@/app/constants/api_properties";
import CompareLineChartCard from "@/app/components/CompareLineChartComponent";

export default function Compare() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [input, setInput] = useState<string | null>(
    searchParams.get("company")
  );
  const [input2, setInput2] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({
    symbol: "",
    marketCap: null,
    reportedEPS: null,
    totalRevenue: null,
    profit: null,
    ppe: null,
  });
  const [data2, setData2] = useState({
    symbol: "",
    marketCap: null,
    reportedEPS: null,
    totalRevenue: null,
    profit: null,
    ppe: null,
  });
  const [comp, setComparisonData] = useState({
    marketCap: null,
    reportedEPS: null,
    totalRevenue: null,
    profit: null,
    ppe: null,
  });
  const [chartData, setChartData] = useState([]);
  const [chartData2, setChartData2] = useState([]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };
  const handleInputChange2 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput2(event.target.value);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/compare?ticker1=${input}&ticker2=${input2}`
        );
        const data = await response.json();
        setLoading(false);

        if (!response.ok) {
          setError(
            `Error: ${
              data.error || "An unexpected error occurred"
            } for inputs "${input}" and "${input2}"`
          );
          return;
        }

        setData({
            reportedEPS: data.ticker1.NEXT_PUBLIC_REPORTED_EPS,
            totalRevenue: data.ticker1.NEXT_PUBLIC_TOTAL_REVENUE,
            profit: data.ticker1.NEXT_PUBLIC_PROFIT,
            ppe: data.ticker1.NEXT_PUBLIC_PPE,
            symbol: data.ticker1.NEXT_PUBLIC_SYMBOL,
            marketCap: data.ticker1.NEXT_PUBLIC_MARKET_CAP,
        });

        setData2({
            reportedEPS: data.ticker2.NEXT_PUBLIC_REPORTED_EPS,
            totalRevenue: data.ticker2.NEXT_PUBLIC_TOTAL_REVENUE,
            profit: data.ticker2.NEXT_PUBLIC_PROFIT,
            ppe: data.ticker2.NEXT_PUBLIC_PPE,
            symbol: data.ticker2.NEXT_PUBLIC_SYMBOL,
            marketCap: data.ticker2.NEXT_PUBLIC_MARKET_CAP,
        });

        setComparisonData({
            reportedEPS: data.COMPARISON.NEXT_PUBLIC_REPORTED_EPS,
            totalRevenue: data.COMPARISON.NEXT_PUBLIC_TOTAL_REVENUE,
            profit: data.COMPARISON.NEXT_PUBLIC_PROFIT,
            ppe: data.COMPARISON.NEXT_PUBLIC_PPE,
            symbol: data.COMPARISON.NEXT_PUBLIC_SYMBOL,
            marketCap: data.COMPARISON.NEXT_PUBLIC_MARKET_CAP,
        });

        const dates1 = data.ticker1.NEXT_PUBLIC_DATE;
        const closes1 = data.ticker1.NEXT_PUBLIC_CLOSE;
        const formattedChartData1 = dates1.map((date, index) => ({
          date,
          close: closes1[index],
        }));
        setChartData(formattedChartData1);

        const dates2 = data.ticker2.NEXT_PUBLIC_DATE;
        const closes2 = data.ticker2.NEXT_PUBLIC_CLOSE;
        const formattedChartData2 = dates2.map((date, index) => ({
          date,
          close: closes2[index],
        }));
        setChartData2(formattedChartData2);

        setError(null);
      } catch (error) {
        console.error("Error getting stock data:", error);
        setError("Failed to fetch stock data");
      }
    };

    if (input && input2) {
      fetchData();
    }
  }, [input, input2]);

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
              <form className="d-flex align-items-center">
                <input
                  className="form-control my-4 w-50 fs-5"
                  type="text"
                  placeholder={`${input}`}
                  aria-label="Search"
                  value={input || ""}
                  onChange={handleInputChange}
                />
                <p className="fs-5 m-4">vs.</p>
                <input
                  className="form-control my-4 w-50 fs-5"
                  type="text"
                  placeholder="Company or Stock Symbol 2"
                  aria-label="Search"
                  value={input2 || ""}
                  onChange={handleInputChange2}
                />
              </form>
              <CompareLineChartCard
                title={`${data.symbol} vs. ${data2.symbol}`}
                dataToDisplay={[...chartData]}
                dataToDisplay2={[...chartData2]}
                xKey="date"
                yKey="close"
                input={input || ""}
                input2={input2 || ""}
              />
              <div className="card fs-4 p-4 shadow-sm mt-4">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col"></th>
                      <th scope="col">{data.symbol}</th>
                      <th scope="col">{data2.symbol}</th>
                      <th scope="col">Difference</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">Market Cap</th>
                      <td>{data.marketCap}</td>
                      <td>{data2.marketCap}</td>
                      <td>{comp.marketCap}</td>
                    </tr>
                    <tr>
                      <th scope="row">Reported EPS</th>
                      <td>{data.reportedEPS}</td>
                      <td>{data2.reportedEPS}</td>
                      <td>{comp.reportedEPS}</td>
                    </tr>
                    <tr>
                      <th scope="row">Revenue</th>
                      <td>{data.totalRevenue}</td>
                      <td>{data2.totalRevenue}</td>
                      <td>{comp.totalRevenue}</td>
                    </tr>
                    <tr>
                      <th scope="row">Profit</th>
                      <td>{data.profit}</td>
                      <td>{data2.profit}</td>
                      <td>{comp.profit}</td>
                    </tr>
                    <tr>
                      <th scope="row">PPE</th>
                      <td>{data.ppe}</td>
                      <td>{data2.ppe}</td>
                      <td>{comp.ppe}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
}
