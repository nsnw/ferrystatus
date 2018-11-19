import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import SailingsTable from "./SailingsTable";
const Sailings = () => (
  <DataProvider endpoint="api/sailings" 
                render={data => <SailingsTable data={data.response} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<Sailings />, wrapper) : null;
