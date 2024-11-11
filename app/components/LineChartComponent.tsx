import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { axisClasses } from "@mui/x-charts";
import { motion } from "framer-motion";

//import { dataset } from "./basicDataset";

//const reversedDataset = [...dataset].reverse();

export default function LineChartCard({ title, dataToDisplay, xKey, yKey }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.8,

        ease: [0, 0.71, 0.2, 1.01],
      }}
      className="card shadow-sm align-items-center w-100"
      style={{ height: 600 }}
    >
      <h2 className="pt-4">{title}</h2>
      <LineChart
        margin={{ left: 80 }}
        sx={{
          [`.${axisClasses.left} .${axisClasses.label}`]: {
            // Move the y-axis label with CSS
            transform: "translateX(-15px)",
          },
        }}
        grid={{ vertical: true, horizontal: true }}
        dataset={[...dataToDisplay]}
        xAxis={[
          {
            scaleType: "point",
            reversed: false,
            dataKey: xKey,
            tickInterval(value, index) {
              return index % 25 === 0;
            },
          },
        ]}
        yAxis={[{ label: "Dollar Amount" }]}
        series={[
          {
            dataKey: yKey,
            color: "#EFBF04",
            showMark: false,
          },
        ]}
      />
    </motion.div>
  );
}
