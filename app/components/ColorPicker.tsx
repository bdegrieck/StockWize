import React, { useState, useEffect } from "react";

interface ColorPickerProps {
  defaultColor?: string;
  onChange: (color: string) => void;
}

const ColorPicker: React.FC<ColorPickerProps> = ({
  defaultColor = "#00FF00",
  onChange,
}) => {
  const [color, setColor] = useState(defaultColor);

  useEffect(() => {
    setColor(defaultColor);
  }, [defaultColor]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newColor = event.target.value;
    setColor(newColor);
    onChange(newColor);
  };

  return (
    <div className="color-picker-cotainer">
      <input
        type="color"
        style={{
          width: "40px",
          height: "40px",
          padding: "5px",
          border: "none",
          transition: "0.25 ease",
        }}
        value={color}
        onChange={handleChange}
      />
    </div>
  );
};

export default ColorPicker;
