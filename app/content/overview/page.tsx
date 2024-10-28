"use client";

import { TextBox, TextBoxContainer } from "@/app/components/TextBox";
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { LineChart } from "@mui/x-charts/LineChart";
import { NEXT_PUBLIC_CLOSE, NEXT_PUBLIC_DATE, NEXT_PUBLIC_DESCRIPTION, NEXT_PUBLIC_MARKET_CAP, NEXT_PUBLIC_YEAR_HIGH, NEXT_PUBLIC_YEAR_LOW } from "@/app/constants/api_properties";

export default function Overview() {
    const searchParams = useSearchParams();
    const input = searchParams.get('company');
    const [error, setError] = useState(null);

    const [data, setData] = useState({
       high: null,
       low: null,
       marketCap: null,
       description: "",
    });

    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/overview?company=${input}`);
                const data = await response.json();

                if (!response.ok) {
                    setError(`Error: ${data.error || "An unexpected error occurred"} for input "${input}"`);
                    return;
                }

                setData({
                    high: data[NEXT_PUBLIC_YEAR_HIGH],
                    low: data[NEXT_PUBLIC_YEAR_LOW],
                    marketCap: data[NEXT_PUBLIC_MARKET_CAP],
                    description: data[NEXT_PUBLIC_DESCRIPTION]
                });

                const dates = data[NEXT_PUBLIC_DATE];
                const closes = data[NEXT_PUBLIC_CLOSE];
                const formattedChartData = dates.map((date, index) => ({
                    date,
                    close: closes[index]
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
        <div className="container-fluid h-100 d-flex flex-column gap-3">
            {error ? (
                // Display error if it exists
                <div style={{ color: 'red', textAlign: 'center', fontWeight: 'bold' }}>
                    {error}
                </div>
            ) : (
                <>
                    <TextBoxContainer>
                        <TextBox title="52 Week High" body={`$${data.high}`} centerText={true} />
                        <TextBox title="52 Week Low" body={`$${data.low}`} centerText={true} />
                        <TextBox title="Market Cap" body={data.marketCap ? data.marketCap.toLocaleString() : ""} centerText={true} />
                    </TextBoxContainer>
                    <TextBox title="Company Description" body={data.description} />
                    <LineChart
                        width={1250}
                        height={500}
                        grid={{ vertical: true, horizontal: true }}
                        dataset={chartData}
                        xAxis={[{ scaleType: "point", dataKey: "date" }]}
                        series={[{ dataKey: "close", color: "#FF0000", showMark: false }]}
                    />
                </>
            )}
        </div>
    );
}