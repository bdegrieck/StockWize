"use client";

import Link from "next/link";
import Logo from "@/app/assets/images/Logo.png";
import Ball from "@/app/assets/images/Ball.png";
import Binoculars from "@/app/assets/images/Binoculars.png";
import Clock from "@/app/assets/images/Clock.png";
import Eye from "@/app/assets/images/Eye.png";
import Money from "@/app/assets/images/Money.png";
import News from "@/app/assets/images/News.png";
import Scale from "@/app/assets/images/Scale.png";
import Image, { StaticImageData } from "next/image";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import Skeleton from "@mui/material/Skeleton";
import LinearProgress from "@mui/material/LinearProgress";

import { motion } from "framer-motion";
import {
  FUN_FACT,
  LAST_UPDATED,
  NEXT_PUBLIC_SYMBOL,
} from "@/app/constants/api_properties";

export default function ContentLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const searchParams = useSearchParams();
  const pathName = usePathname();
  const router = useRouter();
  const pageName = pathName.split("/content/")[1] || ""; //Hacky way to get the page name, then it is capitalized in the display
  const company =
    searchParams.get("company") === null
      ? ""
      : searchParams.get("company")?.toUpperCase();
  const [query, setQuery] = useState(company);
  const [metadata, setMetadata] = useState({} as any);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [symbol, setSymbol] = useState({});

  const content =
    company === "" ? (
      <div className="h-100 w-100 d-flex justify-content-center align-items-center">
        <p className="fs-4">
          Search for a Company or Stock Symbol to Get Started
        </p>
      </div>
    ) : (
      <div className="h-100 d-flex flex-column">
        <div className="flex-grow-1 d-flex flex-column">{children}</div>
      </div>
    );

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    // This is a temporary solution. In reality, we will need to call backend for data
    // If the company doesn't exist, we need to reroute to a 404 page.
    e.preventDefault();
    router.push(`${pathName}?company=${query}`);
  }

  useEffect(() => {
    async function fetchData() {
      console.log("FetchData running on template");
      console.log("Company Search", searchParams.get("company"));
      const response = await fetch(
        `http://127.0.0.1:5000/api/symbol?company=${company}`
      );
      console.log("Response", response);
      const data = await response.json();
      setSymbol({
        Symbol: data[NEXT_PUBLIC_SYMBOL],
      });
      console.log("data", response[NEXT_PUBLIC_SYMBOL]);
    }
    if (company) {
      fetchData();
    }
  }, [company]);

  useEffect(() => {
    async function fetchMetadata() {
      try {
        setLoading(true);
        const response = await fetch(`http://127.0.0.1:5000/api/metadata`);
        const data = await response.json();

        if (!response.ok) {
          setError(true);
          return;
        }

        setMetadata({
          fun_fact: data[FUN_FACT],
          last_updated: data[LAST_UPDATED],
        });

        setError(false);
        setLoading(false);
      } catch (error) {
        console.error("Error getting stock data:", error);
        setError(true);
      }
    }

    fetchMetadata();
  }, metadata);

  return (
    <>
      <div
        className="d-flex flex-column col-3 vh-100 position-absolute pt-3"
        style={{ width: 350 }}
      >
        <Link href="/" className="mx-3">
          <div className="d-flex flex-row align-items-center">
            <Image src={Logo} alt="StockWize Logo" width={50} />
            <span className="p-2 fs-5 fw-bold companyName">StockWize</span>
          </div>
        </Link>
        {symbol[NEXT_PUBLIC_SYMBOL] ? (
          <h1 className="mt-4 mx-3 col-10 fw-bold display-4">
            {symbol[NEXT_PUBLIC_SYMBOL]}
          </h1>
        ) : (
          <h1 className="mt-4 mx-3 col-10 fw-bold display-4 invisible">
            Ticker
          </h1>
        )}
        <p className="mx-3 col-10 fs-5 text-muted">
          Last Updated {metadata[LAST_UPDATED]}
        </p>
        <div className="flex-grow-1 d-flex pt-2 flex-column col-11 rounded-end bg-light shadow">
          <NavBarItem
            route="/content/overview"
            company={company}
            img={Binoculars}
            text="Overview"
          />

          <NavBarItem
            route="/content/forecasted"
            company={company}
            img={Ball}
            text="Forecasted"
          />
          <NavBarItem
            route="/content/stocknews"
            company={company}
            img={News}
            text="Stock News"
          />
          <NavBarItem
            route="/content/explanatory"
            company={company}
            img={Eye}
            text="Explanatory"
          />
          <NavBarItem
            route="/content/microeconomics"
            company={company}
            img={Money}
            text="Microeconomics"
          />
          <NavBarItem
            route="/content/compare"
            company={company}
            img={Scale}
            text="Compare"
          />
          <div className="flex-fill d-flex justify-content-center align-items-center mx-5">
            {loading ? (
              <>
                {/* <div className="d-flex align-items-center justify-content-center w-100 h-100">
                  <div
                    className="spinner-border text-primary"
                    style={{ width: 50, height: 50 }}
                  ></div>
                </div> */}
                <div className="d-flex flex-column flex-grow-1 align-items-center justify-content-center">
                  <LinearProgress color="inherit" className="w-50" />
                </div>
              </>
            ) : error ? (
              <p>There was an error loading a fun fact</p>
            ) : (
              <p className="fs-5">
                <b>Fun Fact:</b> {metadata[FUN_FACT]}
              </p>
            )}
          </div>
        </div>
      </div>
      <div
        className="d-flex flex-column flex-grow-1 vh-100"
        style={{ marginLeft: 350 }}
      >
        <form onSubmit={onSubmit} className="">
          <input
            className="form-control my-4 w-75 fs-5"
            type="text"
            placeholder="Company or Stock Symbol"
            aria-label="Search"
            value={query ? query : ""}
            onChange={(e) => setQuery(e.target.value)}
          />
        </form>
        <motion.div
          initial={{ opacity: 0, scale: 1 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ ease: "easeInOut", duration: 0.5 }}
          className="rounded-start bg-light shadow h-100 flex-grow-1 p-4 overflow-auto"
        >
          {content}
        </motion.div>
      </div>
    </>
  );
}

function NavBarItem({
  route,
  company,
  img,
  text,
}: {
  route: string;
  company: string | undefined;
  img: StaticImageData;
  text: string;
}) {
  const href = `${route}?company=${company}`;

  if (route === "/content/compare") {
    const href = `${route}?ticker1=${company}&ticker2=`;
  } else if (route === "/content/forecasted") {
    const href = `${route}?company=${company}&days=`;
  } else {
    const href = `${route}?company=${company}`;
  }

  const pathName = usePathname();

  // Can't seem to bootstrap this style, since it must explicitly be declared as background color.
  const background_color = pathName === route ? "#E8E8E8" : "clear";
  return (
    <Link
      href={href}
      className="mt-2 w-100 d-flex align-items-center"
      style={{ backgroundColor: background_color }}
    >
      <Image src={img} alt="StockWize Logo" width={25} className="ms-5 me-2" />
      <span className="p-2 fs-5 companyName">{text}</span>
    </Link>
  );
}
