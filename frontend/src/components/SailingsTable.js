import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";
import { PercentFull } from "./PercentFull"

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
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>(ETA {sailing.eta_or_arrival_time_hour_minute})</i></span>
  else if (sailing.state == "Arrived")
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>({sailing.eta_or_arrival_time_hour_minute})</i></span>
  else
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong></span>
  
  return state;
};

function formatStatusText(sailing) {
  if (sailing.state == "Not departed" && sailing.status && sailing.status != "On Time")
    return <td colSpan="5"><small> → {sailing.status}</small></td>
};

const AllSailingsTable = ({ data }) =>
  !data.length ? (
    <p>No sailings found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>All sailings</strong>
      </h1>
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
            <>
            <tr key={el.id}>
              <td><Link to={`/sailings/${el.id}`}><strong>{el.route}</strong></Link></td>
              <td>{formatDeparture(el)}</td>
              <td>{formatStatus(el)}</td>
              <td><strong>{el.ferry}</strong></td>
              <td>{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</td>
            </tr>
            <tr>{formatStatusText(el)}</tr>
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
AllSailingsTable.propTypes = {
  data: PropTypes.array.isRequired
};

const RouteSailingsTable = ({ data }) =>
  !data.length ? (
    <p>No sailings found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>Sailings for {data[0].route}</strong>
      </h1>
      <h3 className="subtitle">
        <Link to="/sailings"><strong className="has-text-link">All sailings</strong></Link>
      </h3>
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
            <>
            <tr key={el.id}>
              <td><Link to={`/sailings/route/${el.route_id}`}><strong>{el.route}</strong></Link></td>
              <td>{el.scheduled_departure_hour_minute}</td>
              <td><Link to={`/sailings/${el.id}`}><strong className={"has-text-" + getDepartedStateColour(el.state)}>{el.state}</strong></Link></td>
              <td><strong>{el.ferry}</strong></td>
              <td>{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</td>
            </tr>
            <tr>{formatStatusText(el)}</tr>
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
RouteSailingsTable.propTypes = {
  data: PropTypes.array.isRequired
};
export { RouteSailingsTable, AllSailingsTable };
