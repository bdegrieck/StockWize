"use client";

import { TextBox, TextBoxContainer } from "@/app/components/TextBox";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
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
  NEXT_PUBLIC_PPE,
  TICKER_1_DATA,
  TICKER_2_DATA,
  COMPARISON,
  NEXT_PUBLIC_TOTAL_REVENUE,
  NEXT_PUBLIC_PROFIT,
} from "@/app/constants/api_properties";
import CompareLineChartCard from "@/app/components/CompareLineChartComponent";
import { useRouter } from "next/navigation";
import ColorPicker from "@/app/components/ColorPicker";

export default function Compare() {
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const [ticker1, setTicker1] = useState(searchParams.get("ticker1") || "");
  const [ticker2, setTicker2] = useState(searchParams.get("ticker2") || "");

  const handleTempInputChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setTicker1(event.target.value);
  };
  const handleTempInputChange2 = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setTicker2(event.target.value);
  };

  const [data, setData] = useState({
    symbol: "",
    marketCap: null,
    reportedEPS: null,
    revenue: null,
    profit: null,
    ppe: null,
    dates: null,
    close_prices: null,
  });

  const [data2, setData2] = useState({
    symbol: "",
    marketCap: null,
    reportedEPS: null,
    revenue: null,
    profit: null,
    ppe: null,
    dates: null,
    close_prices: null,
  });

  const [compData, setCompData] = useState({
    marketCap: null,
    reportedEPS: null,
    revenue: null,
    profit: null,
    ppe: null,
    dates: null,
    close_prices: null,
  });

  const [chartData, setChartData] = useState([]);
  const [chartData2, setChartData2] = useState([]);

  const [selectedColor1, setSelectedColor1] = useState("#EFBF04");
  const [selectedColor2, setSelectedColor2] = useState("#EF9504");

  const fetchData = async (setData, setChartData) => {
    try {
      setLoading(true);
      const response = await fetch(
        `http://127.0.0.1:5000/api/comparison?ticker1=${ticker1}&ticker2=${ticker2}`
      );
      const resp = await response.json();
      setLoading(false);

      if (!response.ok) {
        setError(
          `Error: ${
            resp.error || "An unexpected error occurred"
          } for inputs: "${ticker1}" and "${ticker2}"`
        );
        return;
      }

      setData({
        symbol: resp[TICKER_1_DATA][NEXT_PUBLIC_SYMBOL],
        marketCap: resp[TICKER_1_DATA][NEXT_PUBLIC_MARKET_CAP].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        reportedEPS: resp[TICKER_1_DATA][NEXT_PUBLIC_REPORTED_EPS].toFixed(2),
        revenue: resp[TICKER_1_DATA][NEXT_PUBLIC_TOTAL_REVENUE].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        profit: resp[TICKER_1_DATA][NEXT_PUBLIC_PROFIT].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        ppe: resp[TICKER_1_DATA][NEXT_PUBLIC_PPE].toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
        }),
        dates: resp[TICKER_1_DATA][NEXT_PUBLIC_DATE],
        close_prices: resp[TICKER_1_DATA][NEXT_PUBLIC_CLOSE],
      });

      setData2({
        symbol: resp[TICKER_2_DATA][NEXT_PUBLIC_SYMBOL],
        marketCap: resp[TICKER_2_DATA][NEXT_PUBLIC_MARKET_CAP].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        reportedEPS: resp[TICKER_2_DATA][NEXT_PUBLIC_REPORTED_EPS].toFixed(2),
        revenue: resp[TICKER_2_DATA][NEXT_PUBLIC_TOTAL_REVENUE].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        profit: resp[TICKER_2_DATA][NEXT_PUBLIC_PROFIT].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        ppe: resp[TICKER_2_DATA][NEXT_PUBLIC_PPE].toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
        }),
        dates: resp[TICKER_2_DATA][NEXT_PUBLIC_DATE],
        close_prices: resp[TICKER_2_DATA][NEXT_PUBLIC_CLOSE],
      });

      setCompData({
        marketCap: resp[COMPARISON][NEXT_PUBLIC_MARKET_CAP].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        reportedEPS: resp[COMPARISON][NEXT_PUBLIC_REPORTED_EPS].toFixed(2),
        revenue: resp[COMPARISON][NEXT_PUBLIC_TOTAL_REVENUE].toLocaleString(
          "en-US",
          {
            style: "currency",
            currency: "USD",
          }
        ),
        profit: resp[COMPARISON][NEXT_PUBLIC_PROFIT].toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
        }),
        ppe: resp[COMPARISON][NEXT_PUBLIC_PPE].toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
        }),
      });

      const dates = resp[TICKER_1_DATA][NEXT_PUBLIC_DATE];
      const closes = resp[TICKER_1_DATA][NEXT_PUBLIC_CLOSE];
      const formattedChartData = dates.map((date, index) => ({
        date,
        close: closes[index] || 0,
      }));
      setChartData(formattedChartData);

      const dates2 = resp[TICKER_2_DATA][NEXT_PUBLIC_DATE];
      const closes2 = resp[TICKER_2_DATA][NEXT_PUBLIC_CLOSE];
      const formattedChartData2 = dates2.map((date, index) => ({
        date,
        close: closes2[index] || 0,
      }));

      setChartData2(formattedChartData2);

      setError(null);
    } catch (error) {
      console.error("Error getting stock data:", error);
      if (ticker1 != "" && ticker2 != "") {
        setError(`There was an error fetching data for ${ticker1} and ${ticker2}. Please ensure these are valid stock ticker.`);
      }
      else if (ticker1 != "" && ticker2 == "") {
        setError(
          `There was an error fetching data for ${ticker1}. Please ensure this is a valid stock ticker.`
        );
      } else if (ticker1 == "" && ticker2 != "") {
        setError(
          `There was an error fetching data for ${ticker2}. Please ensure this is a valid stock ticker.`
        );
      } else setError("Failed to fetch stock data");
    }
  };

  const handleCompare = () => {
    router.replace(`/content/compare?ticker1=${ticker1}&ticker2=${ticker2}`);
    if (ticker1) {
      fetchData(setData, setChartData);
    }
    if (ticker2) {
      fetchData(setData2, setChartData2);
    }
  };

  return (
    <div className="container-fluid h-100 d-flex flex-column gap-3 pb-5">
      <form className="d-flex align-items-center">
        <input
          className="form-control my-4 w-50 fs-5"
          type="text"
          placeholder="Enter Company Name or Symbol"
          aria-label="Search"
          value={ticker1}
          onChange={handleTempInputChange}
        />
        <ColorPicker
          defaultColor={selectedColor1}
          onChange={(color) => setSelectedColor1(color)}
        />
        <p className="fs-5 m-4">vs.</p>
        <input
          className="form-control my-4 w-50 fs-5"
          type="text"
          placeholder="Enter Company Name or Symbol"
          aria-label="Search"
          value={ticker2}
          onChange={handleTempInputChange2}
        />
        <ColorPicker
          defaultColor={selectedColor2}
          onChange={(color) => setSelectedColor2(color)}
        />
        <button
          type="button"
          className="btn btn-warning text-black ms-4 fs-5"
          onClick={handleCompare}
        >
          Compare
        </button>
      </form>
      {error ? (
        // Display error if it exists
        <div style={{ color: "red", textAlign: "center", fontWeight: "bold" }}>
          {error}
        </div>
      ) : (
        <>
          {loading ? (
            <>
              <div className="d-flex align-items-center justify-content-center w-100 h-100">
                <div
                  className="spinner-border text-primary"
                  style={{ width: 100, height: 100 }}
                ></div>
              </div>
            </>
          ) : (
            <CompareLineChartCard
              title={`${data.symbol} vs. ${data2.symbol}`}
              dataToDisplay={[...chartData].reverse()}
              dataToDisplay2={[...chartData2].reverse()}
              xKey="date"
              yKey="close"
              input={data.symbol}
              input2={data2.symbol}
              color1={selectedColor1}
              color2={selectedColor2}
            />
          )}
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
                  <td>{compData.marketCap}</td>
                </tr>
                <tr>
                  <th scope="row">Reported EPS</th>
                  <td>{data.reportedEPS}</td>
                  <td>{data2.reportedEPS}</td>
                  <td>{compData.reportedEPS}</td>
                </tr>
                <tr>
                  <th scope="row">Revenue</th>
                  <td>{data.revenue}</td>
                  <td>{data2.revenue}</td>
                  <td>{compData.revenue}</td>
                </tr>
                <tr>
                  <th scope="row">Profit</th>
                  <td>{data.profit}</td>
                  <td>{data2.profit}</td>
                  <td>{compData.profit}</td>
                </tr>
                <tr>
                  <th scope="row">PPE</th>
                  <td>{data.ppe}</td>
                  <td>{data2.ppe}</td>
                  <td>{compData.ppe}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
