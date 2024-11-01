"use client";

import React, { useEffect, useState } from "react";

interface TextBoxProps {
  title: string;
  body: string;
  centerText?: boolean;
}

const TextBox: React.FC<TextBoxProps> = ({
  title,
  body,
  centerText = false,
}) => {
  const textAlignClass = centerText ? "text-center" : "";

  const [fontSize, setFontSize] = useState<string | null>(null);

  useEffect(() => {
    const handleResize = () => {
      const boxWidth = document.querySelector(".card")?.clientWidth || 0;
      setFontSize(`${boxWidth / 12}px`);
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="card flex-grow-1 w-100 gap-3 shadow-sm">
      <div className={`card-body ${textAlignClass}`}>
        {fontSize && (
          <>
            <h2 className="fw-bold">{title}</h2>
            <p className="card-text fs-4">{body}</p>
          </>
        )}
      </div>
    </div>
  );
};

interface TextBoxContainerProps {
  children: React.ReactNode;
}

const TextBoxContainer: React.FC<TextBoxContainerProps> = ({ children }) => {
  return <div className="d-flex w-100 flex-fill gap-3">{children}</div>;
};

export { TextBox, TextBoxContainer };
