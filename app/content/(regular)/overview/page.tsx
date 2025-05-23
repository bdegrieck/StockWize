"use client";

import { TextBox, TextBoxContainer } from "@/app/components/TextBox";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import LineChartCard from "@/app/components/LineChartComponent";
import {
  NEXT_PUBLIC_CLOSE,
  NEXT_PUBLIC_DATE,
  NEXT_PUBLIC_DESCRIPTION,
  NEXT_PUBLIC_MARKET_CAP,
  NEXT_PUBLIC_YEAR_HIGH,
  NEXT_PUBLIC_YEAR_LOW,
} from "@/app/constants/api_properties";
import SkeletonTextBox from "@/app/components/SkeletonTextBox";
import SkeletonLineChart from "@/app/components/SkeletonLineChart";
import LinearProgress from "@mui/material/LinearProgress";

export default function Overview() {
  const searchParams = useSearchParams();
  const input = searchParams.get("company");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const [data, setData] = useState({
    high: null,
    low: null,
    marketCap: null,
    description: "",
  });

  const [chartData, setChartData] = useState([]);

  // Use to get the company name
  // function getCompanyName(description: string): string {
  //   if (!description) return "";
  //   const tokens = description.split(",");
  //   return tokens[0].trim();
  // }

  // const companyName = getCompanyName(data.description);

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
          high: data[NEXT_PUBLIC_YEAR_HIGH].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          low: data[NEXT_PUBLIC_YEAR_LOW].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          marketCap: data[NEXT_PUBLIC_MARKET_CAP].toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          }),
          description: data[NEXT_PUBLIC_DESCRIPTION],
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
              {/* <div className="d-flex align-items-center justify-content-center w-100 h-100">
                <div
                  className="spinner-border text-primary m-3"
                  style={{ width: 100, height: 100 }}
                ></div>
              </div> */}
              <div className="d-flex flex-column flex-grow-1 align-items-center justify-content-center">
                <p className="fw-light fs-4 pb-3 text-muted">L O A D I N G</p>
                <LinearProgress color="inherit" className="w-50" />
              </div>
              {/* 
              
              If we want a skeleton loader, here is a sample:
              
              <SkeletonLineChart />
              <div className="d-flex h-25">
                <SkeletonTextBox />
                <SkeletonTextBox />
                <SkeletonTextBox />
              </div>
              <SkeletonTextBox /> */}
            </>
          ) : (
            <>
              <LineChartCard
                title="Stock Price"
                dataToDisplay={[...chartData].reverse()}
                xKey="date"
                yKey="close"
              />
              <TextBoxContainer>
                <TextBox
                  title="52 Week High"
                  body={data.high}
                  centerText={true}
                />
                <TextBox
                  title="52 Week Low"
                  body={data.low}
                  centerText={true}
                />
                <TextBox
                  title="Market Cap"
                  body={data.marketCap ? data.marketCap : ""}
                  centerText={true}
                />
              </TextBoxContainer>
              <TextBox title="Company Description" body={data.description} />
            </>
          )}
        </>
      )}
    </div>
  );
}
