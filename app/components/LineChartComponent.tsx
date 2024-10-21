import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { dataset } from "./basicDataset";

const reversedDataset = [...dataset].reverse();

export default function SimpleLineChart() {
  return (
    <LineChart
      width={1250}
      height={500}
      grid={{ vertical: true, horizontal: true }}
      dataset={reversedDataset}
      xAxis={[{ scaleType: "point", dataKey: "x" }]}
      series={[{ dataKey: "y", color: "#FF0000" }]}
    />
  );
}