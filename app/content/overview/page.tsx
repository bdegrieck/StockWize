"use client";

import { TextBox, TextBoxContainer } from "@/app/components/TextBox";
import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { LineChart } from "@mui/x-charts/LineChart";

export default function Overview() {
    const searchParams = useSearchParams();
    const input = searchParams.get('company');

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
                const response = await fetch(`http://127.0.0.1:5000/api/stock?company=${input}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();

                setData({
                    high: data[process.env.NEXT_PUBLIC_YEAR_HIGH],
                    low: data[process.env.NEXT_PUBLIC_YEAR_LOW],
                    marketCap: data[process.env.NEXT_PUBLIC_MARKET_CAP],
                    description: data[process.env.NEXT_PUBLIC_DESCRIPTION]
                });

                // Assuming date and close are arrays
                const dates = data[process.env.NEXT_PUBLIC_DATE];
                const closes = data[process.env.NEXT_PUBLIC_CLOSE];

                // Map dates and closes to create chart data points
                const formattedChartData = dates.map((date, index) => ({
                    date,
                    close: closes[index]
                }));

                setChartData(formattedChartData);
            } catch (error) {
                console.error("Error getting stock data:", error);
            }
        };

        if (input) {
            fetchData();
        }
    }, [input]);

    return (
        <div className="container-fluid h-100 d-flex flex-column gap-3">
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
              series={[{ dataKey: "close", color: "#FF0000" }]}
            />
        </div>
    );
}