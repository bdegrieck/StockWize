"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  NEXT_PUBLIC_CLOSE,
  NEXT_PUBLIC_DATE,
  FORECAST_DAYS,
  FORECAST,
  NEXT_PUBLIC_SYMBOL,
  FORECAST_DATES
} from "@/app/constants/api_properties";
import LineWithPrediction from "@/app/components/ForecastedGraph";

export default function Forecasted() {
    const searchParams = useSearchParams();
    const router = useRouter();

    // Properly destructure state
    const [company, setCompany] = useState(searchParams.get("company") || "");
    const [days, setDays] = useState(searchParams.get("days") || "");

    const [data, setData] = useState({
        NEXT_PUBLIC_CLOSE: null,
        FORECAST_DATES: null,
        NEXT_PUBLIC_DATE: null,
        FORECAST: null,
        FORECAST_DAYS: null,
        NEXT_PUBLIC_SYMBOL: null
    });

    const [chartData, setChartData] = useState([]);

    const fetchData = async () => {
        try {
            const response = await fetch(
                `http://127.0.0.1:5000/api/forecast?company=${company}&days=${days}`
            );
            const resp = await response.json();

            if (!response.ok) {
                console.error(
                    `Error: ${
                        resp.error || "An unexpected error occurred"
                    } for inputs: "${company}" and "${days}"`
                );
                return;
            }

            setData({
                NEXT_PUBLIC_SYMBOL: resp[NEXT_PUBLIC_SYMBOL],
                FORECAST: resp[FORECAST].toLocaleString("en-US", {
                    style: "currency",
                    currency: "USD",
                }),
                FORECAST_DAYS: resp[FORECAST_DAYS],
                NEXT_PUBLIC_DATE: resp[NEXT_PUBLIC_DATE],
                NEXT_PUBLIC_CLOSE: resp[NEXT_PUBLIC_CLOSE],
                FORECAST_DATES: resp[FORECAST_DATES]
            });

            const dates = resp[NEXT_PUBLIC_DATE];
            const closes = resp[NEXT_PUBLIC_CLOSE];
            const formattedChartData = dates.map((date, index) => ({
                date,
                close: closes[index] || 0,
            }));
            setChartData(formattedChartData);
        } catch (error) {
            console.error("Error getting stock data:", error);
        }
    };

    const handleForecast = () => {
        if (!company || !days) {
            alert("Please select a company and number of days!");
            return;
        }
        // Use state values directly
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
            <p>
                How many days into the future would you like to predict? Note -
                The further out, the less accurate the prediction will become!
            </p>
            <div className="d-flex flex-row align-items-center">
                <select
                    className="form-select mb-3 me-3"
                    aria-label="Default select example"
                    value={days}
                    onChange={(e) => setDays(e.target.value)}
                >
                    {options}
                </select>
                <button
                    className="btn btn-lg btn-primary mb-3"
                    onClick={handleForecast}
                >
                    Submit
                </button>
            </div>
            {/* Add a break here */}
            <div style={{ marginTop: "20px" }}>
                <LineWithPrediction />
            </div>
        </>
    );
}
