"use client";

import "./landingpage.css";
import Link from "next/link";
import BrainLight from "./assets/images/BrainLight.png";
import Logo from "./assets/images/Logo.png";
import Image from "next/image";

import { motion } from "framer-motion";

export default function Home() {
  return (
    <div>
      <div className="d-flex flex-row align-items-center p-3 ">
        <Image src={Logo} alt="StockWize Logo" width={50} />
        <span className="p-2 fs-5 fw-bold companyName">StockWize</span>
      </div>
      <div className="position-absolute top-50 start-50 translate-middle container-sm ">
        <div className="d-flex flex-row justify-content-around">
          <motion.div
            initial={{ x: -50, opacity: 0, scale: 1 }}
            animate={{ x: 0, opacity: 1, scale: 1 }}
            transition={{ ease: "easeInOut", duration: 1 }}
            id="textContainer"
            className="d-flex flex-column justify-content-center pe-5 me-5"
          >
            <h1 className="display-3 pb-3 fw-bold">
              Empower <br /> Your <br /> Investments
            </h1>
            <p className="pb-3">
              Stockwise unlocks your financial potential, empowering you to make
              smarter investment decisions with ease.
            </p>
            <Link href={"content/overview"}>
              <button className="px-5 py-2 btn btn-primary">
                Get Started!
              </button>
            </Link>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 1 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ ease: "easeInOut", duration: 0.8 }}
            id="imageContainer"
            className="ps-5"
          >
            <Image src={BrainLight} alt="StockWize Logo" width={350} />
          </motion.div>
        </div>
      </div>
    </div>
  );
}
