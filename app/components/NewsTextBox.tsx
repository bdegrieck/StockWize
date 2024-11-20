"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function NewsTextBox({ title, link, date_published }) {
  return (
    <motion.div
      initial={{ y: 80, opacity: 0, scale: 1 }}
      animate={{ y: 0, opacity: 1, scale: 1 }}
      transition={{
        duration: 0.8,
        delay: 0.5,
        ease: [0, 0.71, 0.2, 1.01],
      }}
      className="card my-3 shadow-sm"
    >
      <div className="card-body d-flex flex-column px-5">
        <h2 className="py-4 fw-bold">{title}</h2>
        <a
          className="btn btn-primary fs-5 w-25 mb-4"
          href={link}
          role="button"
          target="_blank"
        >
          {date_published}
          Read More
        </a>
      </div>
    </motion.div>
  );
}
