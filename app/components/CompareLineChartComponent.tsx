import * as React from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { axisClasses } from "@mui/x-charts";
import { motion } from "framer-motion";

interface CompareLineChartCardProps {
  title: string;
  dataToDisplay: { [key: string]: any }[];
  dataToDisplay2: { [key: string]: any }[];
  xKey: string;
  yKey: string;
  input: string;
  input2: string;
}

const CompareLineChartCard: React.FC<CompareLineChartCardProps> = ({
  title,
  dataToDisplay,
  dataToDisplay2,
  xKey,
  yKey,
  input,
  input2,
}) => {
  const xValues = dataToDisplay.map((item) => item[xKey]);

  const series1 = dataToDisplay.map((item) => ({
    x: item[xKey],
    y: item[yKey],
  }));

  const series2 = dataToDisplay2.map((item) => ({
    x: item[xKey],
    y: item[yKey],
  }));

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
            transform: "translateX(-15px)",
          },
        }}
        grid={{ vertical: true, horizontal: true }}
        xAxis={[
          {
            scaleType: "point",
            data: xValues,
            tickInterval(value, index) {
              return index % 25 === 0;
            },
          },
        ]}
        yAxis={[{ label: "Dollar Amount" }]}
        series={[
          {
            data: series1.map((item) => item.y),
            color: "#EFBF04",
            showMark: false,
            label: `${input}`,
          },
          {
            data: series2.map((item) => item.y),
            color: "#00FF00",
            showMark: false,
            label: `${input2}`,
          },
        ]}
      />
    </motion.div>
  );
};

export default CompareLineChartCard;
