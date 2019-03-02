import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";
import { PercentFull } from "./PercentFull";
import { BasePage } from "./Base";
import { formatAmenities } from "./Utils";

var moment = require('moment-timezone');

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

const AllRoutesTableInner = ({ data }) =>
  !data.length ? (
    <p>No routes found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>Next sailings</strong>
      </h1>
      <p></p>
      {data.map(el => (
        <div key={el.id} className="row mb-4">
          <div className="col-12 row p-0 m-0">
            <div className="col-10 p-1 pl-3 pt-2 bg-primary">
              <Link to={`/sailings/route/${el.id}`}>
                <strong className="text-white">{el.name}</strong>
              </Link>
            </div>
            <div className="col-2 row p-0 mr-0">
              <div className={"col-6 text-center p-0 pt-1 bg-" + getWaitColour(el.car_waits)}>🚗</div>
              <div className={"col-6 text-center p-0 pt-1 bg-" + getWaitColour(el.oversize_waits)}>🚚</div>
            </div>
          </div>
          <div className="row col-12 p-0 m-0">
            <div className="col-12 row p-0 m-0">
              <div className="col-4 pt-2 pl-1 bg-dark text-white text-center">
                {formatRibbon(el.next_sailing)}
                <Link to={`/sailings/${el.next_sailing.id}`}>
                  <h2><strong className="text-white">{formatDeparture(el.next_sailing)}</strong></h2>
                </Link>
              </div>
              <div className="col-8 row pr-0">
                <div className="col-lg-8 col-12 text-center p-0 pt-1 flex-column justify-content-center card card-block">
                  <h5>
                    {!el.next_sailing.ferry ? ( <strong className="text-black-50">TBC</strong> ) : ( <strong>{el.next_sailing.ferry.name}</strong> )}
                  </h5>
                  {el.next_sailing.ferry ? ( formatAmenities(el.next_sailing.ferry.amenities) ) : ( null )}
                </div>
                <div className="col-lg-4 col-12 p-2 flex-column justify-content-center card card-block">{!el.next_sailing.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.next_sailing.percent_full} /> )}</div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

const AllRoutesTable = ({ data }) =>
  <BasePage data={<AllRoutesTableInner data={data} />} />

AllRoutesTable.propTypes = {
  data: PropTypes.array.isRequired
};

export { AllRoutesTable };
