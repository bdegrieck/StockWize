"use client";

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { LineChart } from "@mui/x-charts/LineChart";
import { NEXT_PUBLIC_SYMBOL, NEXT_PUBLIC_TREND, NEXT_PUBLIC_SEASONAL_7, NEXT_PUBLIC_DATE, NEXT_PUBLIC_SEASONAL_30, NEXT_PUBLIC_SEASONAL_365 } from "@/app/constants/api_properties";

export default function Overview() {
    const searchParams = useSearchParams();
    const input = searchParams.get('company');
    const [error, setError] = useState(null);

    const [data, setData] = useState({
       dates: null,
       symbol: null,
       trend: null,
       seasonal_7: null,
       seasonal_30: null,
       seasonal_365: null,
    });

    const [chartTrend, setTrendData] = useState([]);
    const [chartSeasonal7, setSeasonal7Data] = useState([]);
    const [chartSeasonal30, setSeasonal30Data] = useState([]);
    const [chartSeasonal365, setSeasonal365Data] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/eda?company=${input}`);
                const data = await response.json();

                if (!response.ok) {
                    setError(`Error: ${data.error || "An unexpected error occurred"} for input "${input}"`);
                    return;
                }

                const dates = data[NEXT_PUBLIC_DATE] || [];
                const trends = data[NEXT_PUBLIC_TREND] || [];
                const seasonal_7 = data[NEXT_PUBLIC_SEASONAL_7] || [];
                const seasonal_30 = data[NEXT_PUBLIC_SEASONAL_30] || [];
                const seasonal_365 = data[NEXT_PUBLIC_SEASONAL_365] || [];
                const symbol = data[NEXT_PUBLIC_SYMBOL] || "Unknown Symbol";

                setData({
                    dates,
                    symbol,
                    trend: trends,
                    seasonal_7,
                    seasonal_30,
                    seasonal_365
                });

                if (dates.length > 0) {
                    setTrendData(
                        trends.length > 0
                            ? dates.map((date, index) => ({
                                  date,
                                  trend: trends[index] ?? null
                              }))
                            : []
                    );

                    setSeasonal7Data(
                        seasonal_7.length > 0
                            ? dates.map((date, index) => ({
                                  date,
                                  seasonal_7: seasonal_7[index] ?? null
                              }))
                            : []
                    );

                    setSeasonal30Data(
                        seasonal_30.length > 0
                            ? dates.map((date, index) => ({
                                  date,
                                  seasonal_30: seasonal_30[index] ?? null
                              }))
                            : []
                    );

                    setSeasonal365Data(
                        seasonal_365.length > 0
                            ? dates.map((date, index) => ({
                                  date,
                                  seasonal_365: seasonal_365[index] ?? null
                              }))
                            : []
                    );
                } else {
                    setTrendData([]);
                    setSeasonal7Data([]);
                    setSeasonal30Data([]);
                    setSeasonal365Data([]);
                }

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

    const renderChartOrMessage = (chartData, title, symbol) => (
        chartData.length > 0 ? (
            <>
                <h4>{title}: {symbol ? `(${symbol})` : ''}</h4>
                <LineChart
                    width={1250}
                    height={500}
                    grid={{ vertical: true, horizontal: true }}
                    dataset={chartData}
                    xAxis={[{ scaleType: "point", dataKey: "date" }]}
                    series={[{ dataKey: Object.keys(chartData[0])[1], color: "#FF0000", showMark: false }]}
                />
            </>
        ) : (
            <div style={{ textAlign: 'center', margin: '20px 0', fontStyle: 'italic' }}>
                No data available for {title}.
            </div>
        )
    );

    return (
        <div className="container-fluid h-100 d-flex flex-column gap-3">
            {error ? (
                // Display error if it exists
                <div style={{ color: 'red', textAlign: 'center', fontWeight: 'bold' }}>
                    {error}
                </div>
            ) : (
                <>
                    {renderChartOrMessage(chartTrend, "Trend Chart", data.symbol)}
                    {renderChartOrMessage(chartSeasonal7, "Seasonal 7-Day Chart", data.symbol)}
                    {renderChartOrMessage(chartSeasonal30, "Seasonal 30-Day Chart", data.symbol)}
                    {renderChartOrMessage(chartSeasonal365, "Seasonal 365-Day Chart", data.symbol)}
                </>
            )}
        </div>
    );
}