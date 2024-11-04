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
import { FormEvent, useState } from "react";

import { motion } from "framer-motion";

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
    searchParams.get("company") === null ? "" : searchParams.get("company");
  const [query, setQuery] = useState(company);

  const content =
    company === "" ? (
      <div className="h-100 w-100 d-flex justify-content-center align-items-center">
        <p>Search for a Company or Stock Symbol to Get Started</p>
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
        <h1 className="mt-4 mx-3 col-10 fw-bold display-4">{company}</h1>
        <p className="mx-3 col-10 text-muted">Last Updated {getLastWeekday()}</p>
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
          <div className="flex-fill d-flex justify-content-center align-items-center mx-3">
            <p>Fun fact of the day</p>
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
  company: string | null;
  img: StaticImageData;
  text: string;
}) {
  const href = company === null ? route : `${route}?company=${company}`;
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

function getLastWeekday() {
  let lastDate = new Date();  
  let day = lastDate.getDay();

  if (day === 0) {
      lastDate.setDate(lastDate.getDate() - 2);
  } else if (day === 6) {
      lastDate.setDate(lastDate.getDate() - 1);
  } else {
      lastDate.setDate(lastDate.getDate() - 1);  // For weekdays, just go back one day
  }

  const options: Intl.DateTimeFormatOptions = { month: 'long', day: 'numeric' };
  return lastDate.toLocaleDateString('en-US', options);
}