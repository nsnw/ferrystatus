import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import PercentFull from "./PercentFull"

var headers = {
  'route': "Route",
  'scheduled_departure': "Scheduled departure",
  'state': "Status",
  'ferry': "Ferry"
};

function getDepartedStateColour(value) {
  let state = value;

  if (state == "Not departed")
    return "primary"
  else if (state == "Departed")
    return "danger"
  else
    return "success"
};

const SailingsTable = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        <strong>Sailings</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Route</th>
            <th>Departure time</th>
            <th>Status</th>
            <th>Ferry</th>
            <th width="200px">Full</th>
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              <td><strong>{el.route}</strong></td>
              <td>{el.scheduled_departure}</td>
              <td><strong class={"has-text-" + getDepartedStateColour(el.state)}>{el.state}</strong></td>
              <td><strong>{el.ferry}</strong></td>
              <td>{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
SailingsTable.propTypes = {
  data: PropTypes.array.isRequired
};
export default SailingsTable;
