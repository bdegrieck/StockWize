import type { Metadata } from "next";
import "./globals.scss";
import BootstrapClient from "./components/BootstrapClient";

export const metadata: Metadata = {
  title: "StockWize",
  description: "Empower Your Investments",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
        <BootstrapClient/>
      </body>
    </html>
  );
}
