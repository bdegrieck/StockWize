"use client";

import { TextBox, TextBoxContainer } from "@/app/components/TextBox";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { LineChart } from "@mui/x-charts/LineChart";
import Skeleton from "@mui/material/Skeleton";
import {
NEXT_PUBLIC_CPI,
NEXT_PUBLIC_REAL_GDP,
NEXT_PUBLIC_INFLATION,
NEXT_PUBLIC_RETAIL_SALES,
NEXT_PUBLIC_INTEREST_RATES,
NEXT_PUBLIC_UNEMPLOYMENT_RATE
} from "@/app/constants/api_properties";
import SimpleLineChart from "@/app/components/LineChartComponent";
import SkeletonTextBox from "@/app/components/SkeletonTextBox";

export default function Overview() {
  const searchParams = useSearchParams();
  const input = searchParams.get("company");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const [data, setData] = useState({
    cpi: null,
    real_gdp: null,
    inflation: null,
    retail_sales: null,
    interest_rates: null,
    unemployment_rate: null
  });

  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/micro`
        );
        const data = await response.json();
        setLoading(

        if (!response.ok) {
          setError(
            `Error: ${
              data.error || "An unexpected error occurred"
            } for input "${input}"`
          );

          return;
        }

        setData({
          cpi: data[NEXT_PUBLIC_CPI].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          retail_sales: data[NEXT_PUBLIC_RETAIL_SALES].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          inflation: data[NEXT_PUBLIC_INFLATION].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          real_gdp: data[NEXT_PUBLIC_REAL_GDP].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          interest_rates: data[NEXT_PUBLIC_INTEREST_RATES].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          unemployment_rate: data[NEXT_PUBLIC_UNEMPLOYMENT_RATE].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
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

              {/*
              If we want to do a skeleton loader here is a sample:

              <SimpleLineChart sentData={chartData} />

              <div className="d-flex h-25">
                <SkeletonTextBox />
                <SkeletonTextBox />
                <SkeletonTextBox />
              </div>
              <SkeletonTextBox /> */}
            </>
          ) : (
            <>
              <SimpleLineChart sentData={chartData} />
            </>
          )}
        </>
      )}
    </div>
  );
}