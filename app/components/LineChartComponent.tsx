import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
//import { dataset } from "./basicDataset";

//const reversedDataset = [...dataset].reverse();

export default function SimpleLineChart({ sentData }) {
  return (
    <div className="card shadow-sm align-items-center w-100 h-75">
      <LineChart
        grid={{ vertical: true, horizontal: true }}
        dataset={sentData}
        xAxis={[
          {
            scaleType: "point",
            dataKey: "date",
            tickInterval(value, index) {
              return index % 25 === 0;
            },
          },
        ]}
        series={[
          {
            dataKey: "close",
            color: "#EFBF04",
            showMark: false,
          },
        ]}
      />
    </div>
  );
}
