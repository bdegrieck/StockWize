import * as React from "react";
import {
  LineChart,
  AnimatedLine,
  AnimatedLineProps,
} from "@mui/x-charts/LineChart";
import { motion } from "framer-motion";
import { useChartId, useDrawingArea, useXScale } from "@mui/x-charts/hooks";
import { SxProps, Theme } from "@mui/system";


interface CustomAnimatedLineProps extends AnimatedLineProps {
  limit?: number;
  sxBefore?: SxProps<Theme>;
  sxAfter?: SxProps<Theme>;
}

function CustomAnimatedLine(props: CustomAnimatedLineProps) {
  const { limit, sxBefore, sxAfter, ...other } = props;
  const { top, bottom, height, left, width } = useDrawingArea();
  const scale = useXScale();
  const chartId = useChartId();

  if (limit === undefined) {
    return <AnimatedLine {...other} />;
  }

  const limitPosition = scale(limit); // Convert value to x coordinate.

  if (limitPosition === undefined) {
    return <AnimatedLine {...other} />;
  }

  const clipIdleft = `${chartId}-${props.ownerState.id}-line-limit-${limit}-1`;
  const clipIdRight = `${chartId}-${props.ownerState.id}-line-limit-${limit}-2`;
  return (
    <React.Fragment>
      {/* Clip to show the line before the limit */}
      <clipPath id={clipIdleft}>
        <rect
          x={left}
          y={0}
          width={limitPosition - left}
          height={top + height + bottom}
        />
      </clipPath>
      {/* Clip to show the line after the limit */}
      <clipPath id={clipIdRight}>
        <rect
          x={limitPosition}
          y={0}
          width={left + width - limitPosition}
          height={top + height + bottom}
        />
      </clipPath>
      <g clipPath={`url(#${clipIdleft})`}>
        <AnimatedLine {...other} sx={sxBefore} />
      </g>
      <g clipPath={`url(#${clipIdRight})`}>
        <AnimatedLine {...other} sx={sxAfter} />
      </g>
    </React.Fragment>
  );
}

export default function LineWithPrediction({ xElements, yElements, limit_date }) {
  console.log(limit_date);
  console.log(xElements)
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
      <h2 className="pt-4">ARIMA</h2>
      <LineChart
        width={1250}
        height={500}
        grid={{ vertical: true, horizontal: true }}
        //   dataset={reversedDataset}
        series={[
          {
            type: "line",
            //   dataKey: "y",
            color: "#6fd649",
            data: yElements,
            valueFormatter: (v, i) =>
              `${v}${i.dataIndex > 6 ? " (estimated)" : ""}`,
          },
        ]}
        xAxis={[{ data: xElements, scaleType: "point" }]}
        slots={{ line: CustomAnimatedLine }}
        slotProps={{
          line: {
            limit: limit_date,
            sxAfter: { strokeDasharray: "10 10" },
          } as any,
        }}
      />
    </motion.div>
  );
}