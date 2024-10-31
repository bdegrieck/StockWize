import "./landingpage.css";
import Link from "next/link";
import BrainLight from "./assets/images/BrainLight.png";
import Logo from "./assets/images/Logo.png";
import Image from "next/image";

export default function Home() {
  return (
    <div>
      <div className="p-3">
        <Image src={Logo} alt="StockWize Logo" width={50} />
        <span className="p-2 companyName">StockWize</span>
      </div>
      <div className="position-absolute top-50 start-50 translate-middle container-sm">
        <div className="d-flex flex-row justify-content-around">
          <div id="textContainer" className="d-flex flex-column">
            <h1 className="pb-3 title">
              Empower <br /> Your <br /> Investments
            </h1>
            <p className="pb-3 missionStatement">
              Stockwise unlocks your financial potential, empowering you to make
              smarter investment decisions with ease.
            </p>
            <Link href={"content/overview"}>
              <button className="p-10 w-100 button">Get Started</button>
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
