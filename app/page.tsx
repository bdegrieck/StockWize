// 'use client'

import styles from "./landingpage.module.css";
// import BrainLightLogo from "@/app/components/BrainLight";
import Link from "next/link";
import BrainLight from "./assets/images/BrainLight.png";
import Logo from "./assets/images/Logo.png"
import Image from 'next/image';

export default function Home() {
    return (
      <div>
        <nav className={'p-3'}>
          <Image src={Logo} alt="StockWize Logo" width={50}  />
          <span className={`p-2 ${styles.companyName}` }>StockWize</span>
        </nav>
        <div className={`position-absolute top-50 start-50 translate-middle container-sm`}>
          <div className={'d-flex flex-row justify-content-around'}>
            <div id= "textContainer" className={`d-flex flex-column`}>
              <h1 className={`pb-3 ${styles.title}`}>Empower <br/> Your <br/> Investments</h1>
              <p className={`pb-3 ${styles.missionStatement} `}>
                Stockwise unlocks your financial potential, 
                empowering you to make smarter investment decisions with ease.
              </p>
              <Link href={'/overview'}>
                <button className={`p-10 w-100 ${styles.button}`} >
                  Search for Stock Tickers & Companies
                </button>
              </Link>
            </div>
            <div id="imageContainer">
              <Image src={BrainLight} alt="StockWize Logo" width={350} />
            </div>
          </div>
        </div>
      </div>
    );
  }
 