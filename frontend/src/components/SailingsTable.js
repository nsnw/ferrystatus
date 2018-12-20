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
    return "info"
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

  if (sailing.status == "Cancelled")
    state = <span class="tag is-danger is-normal"><strong className="has-text-white">Cancelled</strong></span>
  else
    if (sailing.state == "Departed")
      state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>(ETA {sailing.eta_or_arrival_time_hour_minute})</i></span>
    else if (sailing.state == "Arrived")
      state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>({sailing.eta_or_arrival_time_hour_minute})</i></span>
    else
      state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong></span>
  
  return state;
};

function formatStatusText(sailing) {
  if (sailing.state == "Not departed" && sailing.status != "Cancelled" && sailing.status && sailing.status != "On Time")
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
      {data.map(el => (
        <div key={el.id} className="row mb-4">
          <div className="col-12 row pr-0">
            <div className="col-12 p-1 pl-3 pt-2 bg-primary">
              <Link to={`/sailings/${el.id}`}>
                <strong className="text-white">{el.route}</strong>
              </Link>
            </div>
          </div>
          <div className="row col-12 pr-0">
            <div className="col-12 row pr-0">
              <div className="col-4 pt-2 bg-dark text-white text-center">
                <Link to={`/sailings/${el.id}`}>
                  <h2><strong className="text-white">{el.scheduled_departure_hour_minute}</strong></h2>
                </Link>
              </div>
            </div>
          </div>
          <div className="col-3">{formatDeparture(el)}</div>
          <div className="col-3">{formatStatus(el)}</div>
          <div className="col-6"><strong>{el.ferry}&nbsp;</strong></div>
          <div className="col-6">{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</div>
        </div>
      ))}
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
        <strong>{data[0].route}</strong>
      </h1>
      <h3 className="subtitle">
        <Link to="/sailings"><strong className="has-text-link">All sailings</strong></Link>
      </h3>
      {data.map(el => (
        <div key={el.id} className="columns has-background-white-ter is-multiline">
          <div className="column is-4"><Link to={`/sailings/${el.id}`}><strong>{el.route}</strong></Link></div>
          <div className="column is-2">{formatDeparture(el)}</div>
          <div className="column is-2">{formatStatus(el)}</div>
          <div className="column is-2"><strong>{el.ferry}</strong></div>
          <div className="column is-2">{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</div>
          <div className="column is-12 is-divider is-marginless"></div>
        </div>
      ))}
    </div>
  );
RouteSailingsTable.propTypes = {
  data: PropTypes.array.isRequired
};
export { RouteSailingsTable, AllSailingsTable };
