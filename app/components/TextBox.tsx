import React from "react";
import { motion } from "framer-motion";

interface TextBoxProps {
  title: string;
  body: string;
  centerText?: boolean;
}

const TextBox: React.FC<TextBoxProps> = ({ title, body, centerText = false }) => {
  const textAlignClass = centerText ? "text-center" : "";

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.8,
        ease: [0, 0.71, 0.2, 1.01],
      }}
      className="card flex-grow-1 w-100 gap-3 shadow-sm"
    >
      <div className={`card-body ${textAlignClass}`}>
        <h2 className="fw-bold">{title}</h2>
        <p className="card-text fs-4">{body}</p>
      </div>
    </motion.div>
  );
};

interface TextBoxContainerProps {
  children: React.ReactNode;
}

const TextBoxContainer: React.FC<TextBoxContainerProps> = ({ children }) => {
  return <div className="d-flex w-100 flex-fill gap-3">{children}</div>;
};

export { TextBox, TextBoxContainer };
