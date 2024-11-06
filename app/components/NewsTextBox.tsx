"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function NewsTextBox({ title, link }) {
  return (
    <motion.div
      initial={{ x: 80, opacity: 0, scale: 1 }}
      animate={{ x: 0, opacity: 1, scale: 1 }}
      transition={{
        duration: 0.8,
        delay: 0.5,
        ease: [0, 0.71, 0.2, 1.01],
      }}
      className="card flex-grow-1 w-100 m-2 shadow-sm "
      style={{ height: 150 }}
    >
      <div className="card-body d-flex justify-content-between align-items-center px-5">
        <h2>{title}</h2>
        <a
          className="btn btn-primary fs-5"
          href={link}
          role="button"
          target="_blank"
        >
          Read More
        </a>
      </div>
    </motion.div>
  );
}
