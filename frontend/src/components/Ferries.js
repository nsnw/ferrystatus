import React from "react";
import DataProvider from "./DataProvider";
import FerriesTable from "./FerriesTable";
const Ferries = () => (
  <DataProvider endpoint="api/ferries" 
                render={data => <FerriesTable data={data.response} />} />
);

export { Ferries }
