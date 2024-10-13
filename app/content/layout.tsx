'use client'

import Link from "next/link";
import Logo from "@/app/assets/images/Logo.png"
import Image from 'next/image';
import "./layout.css"
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { FormEventHandler, useState } from "react";

export default function ContentLayout({
    children
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    const searchParams = useSearchParams()
    const pathName = usePathname()
    const router = useRouter();
    const company = searchParams.get('company')
    const [query, setQuery] = useState('');

    function onSubmit() {
        //This does not work for some reason, but my laptop is about to die
        console.log(query)
        router.push(`${pathName}?company=${query}`)
    }

    return (
        <div>
            <div className="d-flex flex-column col-3 vh-100 position-absolute pt-3">
                <Link href="/" className="mx-3">
                    <div className="d-flex flex-row align-items-center">
                        <Image src={Logo} alt="StockWize Logo" width={50}/>
                        <span className="p-2 companyName">StockWize</span>
                    </div>
                </Link>
                <h1 className="mt-4 mx-3 col-10" style={{fontWeight:'bold'}}>
                    {company} 
                </h1>
                <p style={{color:"grey"}} className="mx-3 col-10">
                    Last Updated Blorptober 32nd
                </p>
                <div className="flex-grow-1 d-flex flex-column col-10 rounded-end grey align-items-center">
                    <Link href={`/content/overview/${company}`} className="mt-2">
                        <span className="p-2 companyName">Overview</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={`/content/historical/${company}`} className="mt-2">
                        <span className="p-2 companyName">Historical</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={`/content/forecasted/${company}`} className="mt-2">
                        <span className="p-2 companyName">Forecasted</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={`/content/stocknews/${company}`} className="mt-2">
                        <span className="p-2 companyName">Stock News</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={`/content/explanatory/${company}`} className="mt-2">
                        <span className="p-2 companyName">Explanatory</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={`/content/microeconomics${company}`} className="mt-2">
                        <span className="p-2 companyName">Microeconomics</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <Link href={`/content/compare${company}`} className="mt-2">
                        <span className="p-2 companyName">Compare</span>
                        <Image src={Logo} alt="StockWize Logo" width={25}/>
                    </Link>
                    <div className="flex-fill d-flex justify-content-center align-items-center">
                        <p >Fun fact of the day</p>
                    </div>
                    
                </div>
            </div>
            <div className="col-10 offset-3">
                <input 
                    className="form-control my-3 w-75" 
                    type="search" 
                    placeholder="Search" 
                    aria-label="Search" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onSubmitCapture={onSubmit}
                />
                {children}
            </div>
        </div>
    );
  }





