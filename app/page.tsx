import Image from "next/image";
import styles from "./page.module.css";
import BrainLight from "./assets/images/BrainLight.png"

export default function Home() {
  return (
    <div>
      <div>
        <h1>Empower Your Investments</h1>
        <p>
          Stockwise unlocks your financial potential, 
          empowering you to make smarter investment decisions with ease.
        </p>
        <button className={styles.button}>
          Search for Stock Tickers & Companies
        </button>
      </div>
      <Image
        src={BrainLight}
        width={500}
        height={500}
        alt="Brain"
      />
    </div>
  );
}
