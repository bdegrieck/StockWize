"use client";

import React, { useEffect, useState } from "react";
import NewsTextBox from "@/app/components/NewsTextBox";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";

export default function StockNews() {
  const searchParams = useSearchParams();
  const company = searchParams.get("company") || "";
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticles = async () => {
      if (!company) return;
      setLoading(true);
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/news?company=${company}`
        );
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error("Error fetching articles:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, [company]);

  if (loading) {
    return (
      <div className="d-flex align-items-center justify-content-center w-100 h-100">
        <div
          className="spinner-border text-primary m-3"
          style={{ width: 100, height: 100 }}
        ></div>
      </div>
    );
  }

  if (articles.length === 0) {
    return <p>No articles available.</p>;
  }

  return (
    <div className="row">
      <motion.div className="col">
        {articles.slice(0, 5).map((article, index) => (
          <NewsTextBox
            key={index}
            title={article.title || "No Title Available"}
            link={article.url || "#"}
          />
        ))}
      </motion.div>
      <div className="col">
        {articles.slice(5, 10).map((article, index) => (
          <NewsTextBox
            key={index}
            title={article.title || "No Title Available"}
            link={article.url || "#"}
          />
        ))}
      </div>
      <div className="pb-10"></div>
    </div>
  );
}
