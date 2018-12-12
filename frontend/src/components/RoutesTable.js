import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";
import { PercentFull } from "./PercentFull"

function randomPercent() {
  return Math.floor((Math.random() * 100));
}

function getDepartedStateColour(value) {
  let state = value;

  if (state == "Not departed")
    return "primary"
  else if (state == "Departed")
    return "danger"
  else
    return "success"
};

function getWaitColour(value) {
  let waits = value;

  if (waits == 0)
    return "success"
  else if (waits == 1 )
    return "warning"
  else if (waits > 1 )
    return "danger"
  else
    return "secondary"
};

function formatDeparture(sailing) {
  var state;

  state = <span className="align-middle">{sailing.scheduled_departure_hour_minute}</span>
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
        <div key={el.id} className="row mb-4">
          <div className="col-12 row pr-0">
            <div className="col-10 p-1 bg-primary">
              <Link to={`/sailings/route/${el.id}`}>
                <strong className="text-white">{el.name}</strong>
              </Link>
            </div>
            <div className="col-2 row p-0 mr-0">
              <div className={"col-6 text-center p-0 bg-" + getWaitColour(el.car_waits)}>🚗</div>
              <div className={"col-6 text-center p-0 bg-" + getWaitColour(el.oversize_waits)}>🚚</div>
            </div>
          </div>
          <div className="row col-12 pr-0">
            <div className="col-12 row pr-0">
              <div className="col-4 pt-2 bg-dark text-white text-center">
                <Link to={`/sailings/${el.next_sailing.id}`}>
                  <h2><strong className="text-white">{formatDeparture(el.next_sailing)}</strong></h2>
                </Link>
              </div>
              <div className="col-8 row pr-0">
                <div className="col-lg-8 col-12 text-center p-0"><h5><strong>{el.next_sailing.ferry}</strong></h5></div>
                <div className="col-lg-4 col-12 p-2">{!el.next_sailing.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.next_sailing.percent_full} /> )}</div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
AllRoutesTable.propTypes = {
  data: PropTypes.array.isRequired
};

export { AllRoutesTable };
