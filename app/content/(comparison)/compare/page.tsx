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
} from "@/app/constants/api_properties";
import CompareLineChartCard from "@/app/components/CompareLineChartComponent";

export default function Compare() {
  const searchParams = useSearchParams();
  const [input, setInput] = useState<string | null>(
    searchParams.get("company")
  );
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const [input2, setInput2] = useState("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };
  const handleInputChange2 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput2(event.target.value);
  };
  const [data, setData] = useState({
    symbol: "",
    dividend: null,
    marketCap: null,
    reportedEPS: null,
    description: "",
  });

  const [data2, setData2] = useState({
    symbol: "",
    dividend: null,
    marketCap: null,
    reportedEPS: null,
    description: "",
  });

  const [chartData, setChartData] = useState([]);
  const [chartData2, setChartData2] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/overview?company=${input}`
        );
        const data = await response.json();
        setLoading(false);

        if (!response.ok) {
          setError(
            `Error: ${
              data.error || "An unexpected error occurred"
            } for input "${input}"`
          );
          return;
        }

        setData({
          symbol: data[NEXT_PUBLIC_SYMBOL],
          dividend: data[NEXT_PUBLIC_DIVIDEND],
          marketCap: data[NEXT_PUBLIC_MARKET_CAP],
          reportedEPS: data[NEXT_PUBLIC_REPORTED_EPS],
          description: data[NEXT_PUBLIC_NAME],
        });

        const dates = data[NEXT_PUBLIC_DATE];
        const closes = data[NEXT_PUBLIC_CLOSE];
        const formattedChartData = dates.map((date, index) => ({
          date,
          close: closes[index],
        }));

        setChartData(formattedChartData);
        setError(null);
      } catch (error) {
        console.error("Error getting stock data:", error);
        setError("Failed to fetch stock data");
      }
    };

    if (input) {
      fetchData();
    }
  }, [input]);

  // Fetch data for input2
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/overview?company=${input2}`
        );
        const data2 = await response.json();
        setLoading(false);

        if (!response.ok) {
          setError(
            `Error: ${
              data.error || "An unexpected error occurred"
            } for input "${input2}"`
          );
          return;
        }

        setData2({
          symbol: data2[NEXT_PUBLIC_SYMBOL],
          dividend: data2[NEXT_PUBLIC_DIVIDEND],
          marketCap: data2[NEXT_PUBLIC_MARKET_CAP],
          reportedEPS: data2[NEXT_PUBLIC_REPORTED_EPS],
          description: data2[NEXT_PUBLIC_NAME],
        });

        const dates = data2[NEXT_PUBLIC_DATE];
        const closes = data2[NEXT_PUBLIC_CLOSE];
        const formattedChartData = dates.map((date, index) => ({
          date,
          close: closes[index],
        }));

        setChartData2(formattedChartData);
        setError(null);
      } catch (error) {
        console.error("Error getting stock data:", error);
        setError("Failed to fetch stock data");
      }
    };

    if (input2) {
      fetchData();
    }
  }, [input2]);
  // Test
  // useEffect(() => {
  //   console.log("chartData:", chartData);
  //   console.log("chartData2:", chartData2);
  // }, [chartData, chartData2]);

  return (
    <div className="container-fluid h-100 d-flex flex-column gap-3 pb-5">
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
                title={`${input} vs. ${input2}`}
                dataToDisplay={[...chartData].reverse()}
                dataToDisplay2={[...chartData2].reverse()}
                xKey="date"
                yKey="close"
                yKey2="close"
                input={input || ""}
                input2={input2 || ""}
              />
              <div className="card fs-4 p-4 shadow-sm mt-4">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col"></th>
                      <th scope="col">{input}</th>
                      <th scope="col">{input2}</th>
                      <th scope="col">Difference</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">Price</th>
                      <td>$100.00</td>
                      <td>$100.00</td>
                      <td>$100.00</td>
                    </tr>
                    <tr>
                      <th scope="row">Market Cap</th>
                      <td>$100.00</td>
                      <td>$100.00</td>
                      <td>$100.00</td>
                    </tr>
                    <tr>
                      <th scope="row">Reported EPS</th>
                      <td>$100.00</td>
                      <td>$100.00</td>
                      <td>$100.00</td>
                    </tr>
                    <tr>
                      <th scope="row">Revenue</th>
                      <td>$100.00</td>
                      <td>$100.00</td>
                      <td>$100.00</td>
                    </tr>
                    <tr>
                      <th scope="row">Profit</th>
                      <td>$100.00</td>
                      <td>$100.00</td>
                      <td>$100.00</td>
                    </tr>
                    <tr>
                      <th scope="row">PPE</th>
                      <td>$100.00</td>
                      <td>$100.00</td>
                      <td>$100.00</td>
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
