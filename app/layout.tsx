import type { Metadata } from "next";
import 'bootstrap/dist/css/bootstrap.css';
import "./globals.css";

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
        {/* <BootstrapClient/> */}
      </body>
    </html>
  );
}
