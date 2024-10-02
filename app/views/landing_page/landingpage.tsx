import Image from "next/image";
import styles from "./landingpage.module.css";
import BrainLightLogo from "@/app/components/BrainLight";

export default function LandingPage() {
    return (
      <div>
        <div className={`center ${styles.firstPageTextContent}`}>
          <div className={`verticalFlex`}>
            <h1 className={`flexItem ${styles.title}`}>Empower <br/> Your <br/> Investments</h1>
            <p className={`flexItem ${styles.missionStatement} `}>
              Stockwise unlocks your financial potential, 
              empowering you to make smarter investment decisions with ease.
            </p>
            <button className={`flexItem ${styles.button}`}>
              Search for Stock Tickers & Companies
            </button>
          </div>
          <div className={styles.brainLight}> 
            <BrainLightLogo/>
          </div>
         
        </div>
        <div>
          {/* Secondary info goes here */}
        </div>
      </div>
    );
  }