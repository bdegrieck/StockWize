"use client";

import React, { useEffect, useState } from "react";
import Skeleton from "@mui/material/Skeleton";

export default function SkeletonTextBox() {
  return (
    <div className="card flex-grow-1 w-100 m-2 shadow-sm">
      <div className="card-body">
        <>
          <Skeleton variant="text" />
          <Skeleton variant="text" />
        </>
      </div>
    </div>
  );
}
