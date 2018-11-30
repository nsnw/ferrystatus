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
      {data.map(el => (
        <div key={el.id} className="columns has-background-white-ter is-multiline">
          <div className="column is-4"><Link to={`/sailings/route/${el.id}`}><strong>{el.name}</strong></Link></div>
          <div className="column is-1">{formatDeparture(el.next_sailing)}</div>
          <div className="column is-2">{el.next_sailing.ferry}</div>
          <div className="column is-3">{!el.next_sailing.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.next_sailing.percent_full} /> )}</div>
          <div className="column is-1">{el.car_waits} 🚗</div>
          <div className="column is-1">{el.oversize_waits} 🚚</div>
          <div className="column is-12 is-divider is-marginless"></div>
        </div>
      ))}
    </div>
  );
AllRoutesTable.propTypes = {
  data: PropTypes.array.isRequired
};

export { AllRoutesTable };
