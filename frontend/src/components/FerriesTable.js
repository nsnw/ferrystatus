import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";
import { BasePage } from "./Base";

var keys = ['name', 'status', 'last_updated'];
var headers = {
  'name': "Ferry",
  'status': "Status",
  'last_updated': "Last updated"
};

function formatStatus(ferry) {
  if (ferry.current_sailing)
    return <Link to={`/sailings/${ferry.current_sailing.id}`}>{ferry.current_sailing.route_name}</Link>
};

const FerriesTableInner = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        <strong>Ferries</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Ferry</th>
            <th>Status</th>
            <th>Route</th>
            <th>Last updated</th>
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              <td>{el.name}</td>
              <td>{el.status}</td>
              <td>{formatStatus(el)}</td>
              <td>{el.last_updated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

const FerriesTable = ({ data }) =>
  <BasePage data={<FerriesTableInner data={data} />} />

FerriesTable.propTypes = {
  data: PropTypes.array.isRequired
};
export default FerriesTable;
