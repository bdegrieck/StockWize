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
import "./layout.css";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { FormEvent, useState } from "react";


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
        <p className="fw-bold">
          {pageName.charAt(0).toUpperCase() + pageName.slice(1)}
        </p>
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
      <div className="d-flex flex-column col-3 vh-100 position-absolute pt-3">
        <Link href="/" className="mx-3">
          <div className="d-flex flex-row align-items-center">
            <Image src={Logo} alt="StockWize Logo" width={50} />
            <span className="p-2 companyName">StockWize</span>
          </div>
        </Link>
        <h1 className="mt-4 mx-3 col-10" style={{ fontWeight: "bold" }}>
          {company}
        </h1>
        <p style={{ color: "grey" }} className="mx-3 col-10">
          Last Updated Blorptober 32nd
        </p>
        <div className="flex-grow-1 d-flex flex-column col-11 rounded-end grey align-items-center">
          <NavBarItem
            route="/content/overview"
            company={company}
            img={Binoculars}
            text="Overview"
          />
          <NavBarItem
            route="/content/historical"
            company={company}
            img={Clock}
            text="Historical"
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
      <div className="col-9 offset-3 d-flex flex-column vh-100">
        <form onSubmit={onSubmit} className="">
          <input
            className="form-control my-3 w-75"
            type="text"
            placeholder="Company or Stock Symbol"
            aria-label="Search"
            value={query ? query : ""}
            onChange={(e) => setQuery(e.target.value)}
          />
        </form>
        <div className="rounded-start grey shadow h-100 flex-grow-1 p-3">
          {content}
        </div>
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
  const background_color = pathName === route ? "#E8E8E8" : "clear";
  return (
    <Link
      href={href}
      className="mt-2 w-100 d-flex align-items-center justify-content-center"
      style={{ backgroundColor: background_color }}
    >
      <span className="p-2 companyName">{text}</span>
      <Image src={img} alt="StockWize Logo" width={25} />
    </Link>
  );
}

