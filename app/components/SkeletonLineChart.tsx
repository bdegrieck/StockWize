"use client";

import React, { useEffect, useState } from "react";
import Skeleton from "@mui/material/Skeleton";

export default function SkeletonLineChart() {
  return (
    <div
      className="card flex-grow-1 w-100 m-2 shadow-sm"
      style={{ height: 700 }}
    >
      <div className="card-body d-flex flex-column align-items-center">
        <>
          <Skeleton variant="text" width={500} height={100} />
          <Skeleton variant="rounded" height={500} />
        </>
      </div>
    </div>
  );
}
