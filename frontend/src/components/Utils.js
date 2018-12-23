import React from "react";
import PropTypes from "prop-types";
import { PercentFull } from "./PercentFull";

var moment = require('moment-timezone');

function formatState(sailing) {
  if (sailing.state == "Arrived")
    return <div>
      <h5>{sailing.ferry}</h5>
      <h1><strong>{sailing.state}</strong> at {sailing.eta_or_arrival_time_hour_minute}</h1>
      <div className="p-2"><PercentFull percentFull={sailing.percent_full} /></div>
    </div>
  else if (sailing.state == "Departed")
    return <div>
      <h5>{sailing.ferry}</h5>
      <h1><strong>{sailing.state}</strong> at {sailing.actual_departure_hour_minute}</h1>
    </div>
  else if (sailing.status == "Cancelled")
    return <div>
      <h5>{sailing.ferry}</h5>
      <h1><strong className="rounded p-1 pl-2 pr-2 text-white bg-danger">Cancelled</strong></h1>
    </div>
  else
    return <div>
      <h5>{sailing.ferry}</h5>
      <h1><strong>{sailing.state}</strong></h1>
      <h5>{sailing.status}</h5>
    </div>
};


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

function formatRibbon(sailing) {

  let ts = moment(new Date(sailing.scheduled_departure*1000)).tz("America/Vancouver");
  let now = moment().tz("America/Vancouver");

  if (sailing.status == "Cancelled")
    return <div className="corner-ribbon red">Cancelled</div>
  else if (sailing.status && sailing.status != "On Time")
    return <div className="corner-ribbon turquoise">Delayed</div>
  else if (sailing.percent_full > 90)
    return <div className="corner-ribbon orange">{sailing.percent_full}% full</div>
  else if (ts.date() != now.date())
    return <div className="corner-ribbon purple">Tomorrow</div>
  else
    return <div className="corner-ribbon green">On time</div>

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

const SailingState = ({ sailing }) =>
  {formatState(sailing)}

SailingState.propTypes = {
  sailing: PropTypes.object.isRequired
};

export { getWaitColour, formatRibbon, formatDeparture, formatStatus, formatState };
