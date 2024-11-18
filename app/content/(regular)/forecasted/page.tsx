"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  NEXT_PUBLIC_CLOSE,
  NEXT_PUBLIC_DATE,
  NEXT_PUBLIC_SYMBOL,
  LIMIT
} from "@/app/constants/api_properties";
import LineWithPrediction from "@/app/components/ForecastedGraph";

export default function Forecasted() {
    const searchParams = useSearchParams();
    const router = useRouter();

    // Properly destructure state
    const [company, setCompany] = useState(searchParams.get("company") || "");
    const [days, setDays] = useState(searchParams.get("days") || "");

    const [data, setData] = useState({});

    const [chartData, setChartData] = useState([]);

    const fetchData = async () => {
        console.log('fetchData() is running...');
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
                Symbol: resp[NEXT_PUBLIC_SYMBOL],
                Close: resp[NEXT_PUBLIC_CLOSE],
                Date: resp[NEXT_PUBLIC_DATE],
                Limit: resp[LIMIT],
            });

            const dates = resp[NEXT_PUBLIC_DATE];
            const closes = resp[NEXT_PUBLIC_CLOSE];
            const formattedChartData = dates.map((date, index) => ({
                date,
                close: closes[index] || 0,
            }));
            setChartData(formattedChartData);
            console.log('NEXT_PUBLIC_DATE:', resp[NEXT_PUBLIC_DATE]);
            console.log('NEXT_PUBLIC_CLOSE:', resp[NEXT_PUBLIC_CLOSE]);

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
        <div style={{ marginTop: "20px" }}>

          {data[NEXT_PUBLIC_DATE] && data[NEXT_PUBLIC_CLOSE] && data[NEXT_PUBLIC_DATE].length > 0 && data[NEXT_PUBLIC_CLOSE].length > 0 ? (
            <LineWithPrediction
              xElements={[...data[NEXT_PUBLIC_DATE]].reverse()}
              yElements={[...data[NEXT_PUBLIC_CLOSE]].reverse()}
            />
          ) : (
            <p style={{ color: "red", textAlign: "center", fontWeight: "bold" }}>
              No data available to generate predictions.
            </p>
          )}
        </div>
      </>
    );
}
