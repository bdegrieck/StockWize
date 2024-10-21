import * as React from "react";
import {
  LineChart,
  AnimatedLine,
  AnimatedLineProps,
} from "@mui/x-charts/LineChart";
import { useChartId, useDrawingArea, useXScale } from "@mui/x-charts/hooks";
import { SxProps, Theme } from "@mui/system";
// import { dataset } from "./TestAAPLData";
// import { dataset } from "./basicDataset";

// const reversedDataset = [...dataset].reverse();
// const xElements = [
//   10.24, 10.23, 10.22, 10.21, 10.18, 10.17, 10.15, 10.14, 10.11, 10.1, 10.09,
//   10.08, 10.07,
// ].reverse();
const xElements = [
  "2024-10-24",
  "2024-10-23",
  "2024-10-22",
  "2024-10-21",
  "2024-10-18",
  "2024-10-17",
  "2024-10-15",
  "2024-10-14",
  "2024-10-11",
  "2024-10-10",
  "2024-10-09",
  "2024-10-08",
  "2024-10-07",
].reverse();
const yElements = [
  231.51, 231.08, 230.9, 233.86, 232.72, 232.43, 233.61, 228.7, 229.3, 227.78,
  225.23, 224.3, 224.5,
].reverse();

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

export default function LineWithPrediction() {
  return (
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
          limit: "2024-10-15",
          sxAfter: { strokeDasharray: "10 10" },
        } as any,
      }}
    />
  );
}