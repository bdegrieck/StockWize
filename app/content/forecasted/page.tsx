"use client"

import "./forecasted.css";
import ForecastedGraph from "@/app/components/ForecastedGraph";

export default function Forecasted() {

    const options = Array.from({ length: 30 }, (_, i) => <option key={i+1} value={i+1}>{i+1}</option>);
    return (
        <>
            <p>How many days into the future would you like to predict? Note - The further out, the less accurate the prediction will become!</p>
            <form className="d-flex flex-row">
                <select className="form-select mb-3 me-3" aria-label="Default select example">
                    {options}
                </select>
                <button>Submit</button> { /*The css wont work on this button for some reason */}
            </form>
            <LineGraph />
        </>
    )
}

function LineGraph() {
    return (
      <div className="graphKPI d-flex flex-column justify-content-between bg-white rounded-3 shadow-lg m-0 p-0">
        <div className="stock-text d-flex align-items-center justify-content-between w-100 p-3">
          <div className="left d-flex align-items-end justify-content-between">
            <h1 className="h1 fw-bold pe-3">Ticker</h1>
            <h2 className="h2">Company</h2>
          </div>
          <div className="right d-flex justify-content-between align-self-end">
            <h3 className="h3 fw-bold pe-3">000.00</h3>
            <p className="p text-secondary">+0.00</p>
          </div>
        </div>
        <div className="descriptor d-flex align-items-center justify-content-between">
          <h3 className="h3 text-secondary ps-3">Chart Type</h3>
        </div>
        <ForecastedGraph />
        {/* <LineChartComponent /> */}
        <div className="metrics d-flex w-100 align-items-center justify-content-evenly p-3">
          <div className="value d-flex align-items-center justify-content-between">
            <h3 className="h3 text-secondary pe-2">Open</h3>
            <h2 className="h2 fw-bold text-dark">000.00</h2>
          </div>
          <div className="value d-flex align-items-center justify-content-between">
            <h3 className="h3 text-secondary pe-2">High</h3>
            <h2 className="h2 fw-bold text-dark">000.00</h2>
          </div>
          <div className="value d-flex align-items-center justify-content-between">
            <h3 className="h3 text-secondary pe-2">Low</h3>
            <h2 className="h2 fw-bold text-dark">000.00</h2>
          </div>
          <div className="value d-flex align-items-center justify-content-between">
            <h3 className="h3 text-secondary pe-2">Close</h3>
            <h2 className="h2 fw-bold text-dark">000.00</h2>
          </div>
        </div>
      </div>
    );
  }