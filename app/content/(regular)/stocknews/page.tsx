import React, { useEffect, useState } from 'react';
import NewsTextBox from "@/app/components/NewsTextBox";
import { useSearchParams } from "next/navigation";

export default function StockNews() {

  const searchParams = useSearchParams();
  const company = searchParams.get("company") === null ? "" : searchParams.get("company");
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/news");  // Replace with your API URL
        const data = await response.json();

        // Format dates in the article data
        const formattedArticles = data.map(article => ({
          ...article,
          publish_date: new Date(article.publish_date).toLocaleDateString("en-US", {
            year: 'numeric', month: 'long', day: 'numeric'
          })
        }));

        setArticles(formattedArticles);
      } catch (error) {
        console.error("Error fetching articles:", error);
      }
    };

    fetchArticles();
  }, []);

  return (
    <>
      {articles.slice(0, 10).map((article, index) => (
        <NewsTextBox
          key={index}
          title={article.title || "No Title Available"}
          link={article.url || "#"}
          date_published={article.publish_date || "No Date Published"}
        />
      ))}
    </>
  );
}