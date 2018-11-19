import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import FerriesTable from "./FerriesTable";
const Ferries = () => (
  <DataProvider endpoint="api/ferries" 
                render={data => <FerriesTable data={data.response} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<Ferries />, wrapper) : null;
