import Link from "next/link";
import Logo from "@/app/assets/images/Logo.png"
import Image from 'next/image';
import "./layout.css"

export default function ContentLayout({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    return (
        <div>
            <div className="d-flex flex-column col-3 vh-100 position-absolute pt-3">
                <Link href="/">
                    <div className="d-flex flex-row align-items-center">
                        <Image src={Logo} alt="StockWize Logo" width={50}/>
                        <span className="p-2 companyName">StockWize</span>
                    </div>
                </Link>
                <h1 className="mt-4" style={{fontWeight:'bold'}}>
                    Some Company
                </h1>
                <p style={{color:"grey"}}>
                    Last Updated Blorptober 32nd
                </p>
                <div className="flex-grow-1 d-flex flex-column col-6 rounded-end grey">
                    <Link href={'/content/overview'}>
                        <span className="p-2 companyName">StockWize</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={'/content/historical'}>
                        <span className="p-2 companyName">Historical</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={'/content/forecasted'}>
                        <span className="p-2 companyName">Forecasted</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={'content/stocknews'}>
                        <span className="p-2 companyName">Stock News</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={'content/explanatory'}>
                        <span className="p-2 companyName">Explanatory</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={'content/microeconomics'}>
                        <span className="p-2 companyName">Microeconomics</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={'/content/compare'}>
                        <span className="p-2 companyName">Compare</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                </div>
            </div>
            <div className="col-10 offset-3">
                {children}
            </div>

        </div>

    );
  }



