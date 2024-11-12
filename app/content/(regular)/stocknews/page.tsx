"use client";

import React, { useEffect, useState } from 'react';
import NewsTextBox from "@/app/components/NewsTextBox";
import { useSearchParams } from "next/navigation";

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
    return <p>Loading...</p>;
  }

  if (articles.length === 0) {
    return <p>No articles available.</p>;
  }

  return (
    <>
      {articles.slice(0, 10).map((article, index) => (
        <NewsTextBox
          key={index}
          title={article.title || "No Title Available"}
          link={article.url || "#"}
        />
      ))}
    </>
  );
}
