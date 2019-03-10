import React from "react";
import DataProvider from "./DataProvider";
import { AllSailingsTable, RouteSailingsTable } from "./SailingsTable";
import SailingDetail from "./SailingDetail";

const AllSailings = (props) => (
  <DataProvider endpoint="/api/sailings"
                render={data => <AllSailingsTable data={data.response} />} />
);

const ReallyAllSailings = (props) => (
  <DataProvider endpoint="/api/all-sailings"
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

export { ReallyAllSailings, AllSailings, RouteSailings, Sailing }
