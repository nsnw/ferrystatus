import React from "react";
import DataProvider from "./DataProvider";
import { AllRoutesTable } from "./RoutesTable";

const AllRoutes = (props) => (
  <DataProvider endpoint="/api/routes"
                render={data => <AllRoutesTable data={data.response} />} />
);

export { AllRoutes }
