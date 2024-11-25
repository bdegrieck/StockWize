"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  NEXT_PUBLIC_CLOSE,
  NEXT_PUBLIC_DATE,
  NEXT_PUBLIC_SYMBOL,
  LIMIT,
  LSTM_VALS,
} from "@/app/constants/api_properties";
import LineWithPrediction from "@/app/components/ForecastedGraph";
import LinearProgress from "@mui/material/LinearProgress";

export default function Forecasted() {
  const searchParams = useSearchParams();
  const router = useRouter();

  // Properly destructure state
  const [company, setCompany] = useState("");
  const [days, setDays] = useState(searchParams.get("days") || "");

  const [data, setData] = useState({});

  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const companyParam = searchParams.get("company");
    if (companyParam) {
      setCompany(companyParam);
    }
  }, [searchParams]);

  const fetchData = async () => {
    console.log("fetchData() is running...");
    try {
      setLoading(true);
      console.log("Company Fetch: ", company);
      const response = await fetch(
        `http://127.0.0.1:5000/api/forecast?company=${company}&days=${days}`
      );
      const resp = await response.json();
      setLoading(false);

      if (!response.ok) {
        setError(
          `Error: ${
            resp.error || "An unexpected error occurred"
          } for inputs: "${company}" and "${days}"`
        );
        return;
      }

      setData({
        Symbol: resp[NEXT_PUBLIC_SYMBOL],
        Close: resp[NEXT_PUBLIC_CLOSE],
        Date: resp[NEXT_PUBLIC_DATE],
        Limit: resp[LIMIT],
        lstm_vals: resp[LSTM_VALS],
      });

      const dates = resp[NEXT_PUBLIC_DATE];
      const closes = resp[NEXT_PUBLIC_CLOSE];
      const formattedChartData = dates.map((date, index) => ({
        date,
        close: closes[index] || 0,
      }));
      setChartData(formattedChartData);
      setError(null);
    } catch (error) {
      console.error("Error getting stock data:", error);
      setError("Failed to fetch stock data");
    }
  };

  const handleForecast = () => {
    if (!company || !days) {
      alert("Please select a company and number of days!");
      return;
    }
    // Use state values directly
    setData({});
    setChartData([]);
    setError(null);
    console.log("Company Router: ", company);
    router.replace(`/content/forecasted?company=${company}&days=${days}`);
    fetchData();
  };

  const options = Array.from({ length: 30 }, (_, i) => (
    <option key={i + 1} value={i + 1}>
      {i + 1}
    </option>
  ));

  return (
    <>
      <h2 className="text-center p-2">Forecast Window (Days): </h2>
      <div className="d-flex flex-row align-items-center justify-content-center">
        <select
          className="form-select form-select-lg mb-3 me-3 w-25"
          aria-label="Default select example"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        >
          <option value="">Select Days</option>
          {options}
        </select>
        <button
          className="btn btn-lg btn-primary mb-3"
          onClick={handleForecast}
        >
          Submit
        </button>
      </div>
      <p className="text-center text-muted pb-4">
        Disclaimer: The following are forecast models and do not guarantee
        accuracy.
      </p>

      {loading ? (
        error ? (
          <div
            style={{ color: "red", textAlign: "center", fontWeight: "bold" }}
          >
            {error}
          </div>
        ) : (
          // <div className="d-flex align-items-center justify-content-center w-100 h-100">
          //   {/* <div
          //     className="spinner-border text-primary"
          //     style={{ width: 100, height: 100 }}
          //   ></div> */}

          // </div>
          <div className="d-flex flex-column flex-grow-1 align-items-center justify-content-center">
            <p className="fw-light fs-4 pb-3">L O A D I N G</p>
            <LinearProgress color="inherit" className="w-50" />
          </div>
        )
      ) : data[NEXT_PUBLIC_DATE] &&
        data[NEXT_PUBLIC_CLOSE] &&
        data[NEXT_PUBLIC_DATE].length > 0 &&
        data[NEXT_PUBLIC_CLOSE].length > 0 ? (
        <LineWithPrediction
          xElements={[...data[NEXT_PUBLIC_DATE]].reverse()}
          yElements={[...data[NEXT_PUBLIC_CLOSE]].reverse()}
          limit_date={data[LIMIT]}
          lstm_vals={[...data[LSTM_VALS]].reverse()}
        />
      ) : (
        <></>
      )}
    </>
  );
}
