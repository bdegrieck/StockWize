import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
//import { dataset } from "./basicDataset";

//const reversedDataset = [...dataset].reverse();

export default function SimpleLineChart({ sentData }) {
  return (
    <div className="card shadow-sm align-items-center w-100 h-75">
      <LineChart
        grid={{ horizontal: true }}
        dataset={[...sentData].reverse()}
        xAxis={[{ scaleType: "point", dataKey: "date" }]}
        series={[{ dataKey: "close", color: "#EFBF04", showMark: false }]}
      />
    </div>
  );
}
