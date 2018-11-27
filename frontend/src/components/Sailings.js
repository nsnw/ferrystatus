import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import { AllSailingsTable, RouteSailingsTable } from "./SailingsTable";
import SailingDetail from "./SailingDetail";

const AllSailings = (props) => (
  <DataProvider endpoint="/api/sailings"
                render={data => <AllSailingsTable data={data.response} />} />
);

const RouteSailings = (props) => (
  <DataProvider endpoint="/api/sailings" routeId={props.match.params.routeId}
                render={data => <RouteSailingsTable data={data.response} />} />
);

const Sailing = (props) => (
  <DataProvider endpoint="/api/sailings" sailingId={props.match.params.sailingId}
                render={data => <SailingDetail data={data.response} />} />
);
//const wrapper = document.getElementById("app");
//wrapper ? ReactDOM.render(<Sailings />, wrapper) : null;
//export default Sailings
export { AllSailings, RouteSailings, Sailing }
