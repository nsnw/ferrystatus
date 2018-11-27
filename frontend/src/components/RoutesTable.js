import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";
import { PercentFull } from "./PercentFull"

function getDepartedStateColour(value) {
  let state = value;

  if (state == "Not departed")
    return "primary"
  else if (state == "Departed")
    return "danger"
  else
    return "success"
};

function formatDeparture(sailing) {
  var state;

  if (sailing.actual_departure)
    state = <span>{sailing.scheduled_departure_hour_minute} <i>({sailing.actual_departure_hour_minute})</i></span>
  else
    state = <span>{sailing.scheduled_departure_hour_minute}</span>

  return state;
};

function formatStatus(sailing) {
  let cssStatus = getDepartedStateColour(sailing.state);
  var state;

  if (sailing.state == "Departed")
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>({sailing.eta_or_arrival_time_hour_minute})</i></span>
  else if (sailing.state == "Arrived")
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>({sailing.eta_or_arrival_time_hour_minute})</i></span>
  else
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong></span>
  
  return state;
};

const AllRoutesTable = ({ data }) =>
  !data.length ? (
    <p>No routes found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>All routes</strong>
      </h1>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Route</th>
            <th>Next sailing</th>
            <th>Ferry</th>
            <th width="200px">Full</th>
            <th colSpan="2">Waits</th>
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              <td><Link to={`/sailings/route/${el.id}`}><strong>{el.name}</strong></Link></td>
              <td>{formatDeparture(el.next_sailing)}</td>
              <td>{el.next_sailing.ferry}</td>
              <td>{!el.next_sailing.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.next_sailing.percent_full} /> )}</td>
              <td>{el.car_waits}</td>
              <td>{el.oversize_waits}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
AllRoutesTable.propTypes = {
  data: PropTypes.array.isRequired
};

export { AllRoutesTable };
