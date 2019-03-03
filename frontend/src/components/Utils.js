import React from "react";
import PropTypes from "prop-types";
import { PercentFull } from "./PercentFull";

var moment = require('moment-timezone');

function formatState(sailing) {
  let ferry_name = sailing.ferry ? sailing.ferry.name : undefined;

  if (sailing.state == "Arrived")
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong>{sailing.state}</strong> at {sailing.eta_or_arrival_time_hour_minute}</h1>
      <div className="p-2"><PercentFull percentFull={sailing.percent_full} /></div>
    </div>
  else if (sailing.state == "Departed")
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong>{sailing.state}</strong> at {sailing.actual_departure_hour_minute}</h1>
    </div>
  else if (sailing.status == "Cancelled")
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong className="rounded p-1 pl-2 pr-2 text-white bg-danger">Cancelled</strong></h1>
    </div>
  else
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong>{sailing.state}</strong></h1>
      <h5>{sailing.status}</h5>
    </div>
};

function formatAmenities(amenities) {
  let amenity_list = [];

  for (var i = 0; i < amenities.length; i++) {
    let amenity = amenities[i];

    switch(amenity) {
      case "Coastal Cafe":
        amenity_list.push(
            <span title={amenity}>🍔</span>
        );
        break;
      case "Pacific Buffet":
        amenity_list.push(
            <span title={amenity}>🍽️</span>
        );
        break;
      case "Coast Cafe Express":
      case "Arbutus Coffee Bar":
        amenity_list.push(
            <span title={amenity}>☕</span>
        );
        break;
      case "Pet Area":
        amenity_list.push(
            <span title={amenity}>🐕</span>
        );
        break;
      case "Seawest Lounge":
        amenity_list.push(
            <span title={amenity}>💺</span>
        );
        break;
      case "Passages Gift Shop":
      case "Passages":
        amenity_list.push(
            <span title={amenity}>🎁</span>
        );
        break;
      case "Kids Zone":
      case "Kids play areas":
        amenity_list.push(
            <span title={amenity}>🧒</span>
        );
        break;
      case "Video Zone":
        amenity_list.push(
            <span title={amenity}>🎮</span>
        );
        break;
      case "Work/study stations":
      case "Work stations":
        amenity_list.push(
            <span title={amenity}>💻</span>
        );
        break;
      case "Mobile charging stations":
        amenity_list.push(
            <span title={amenity}>🔌</span>
        );
        break;
      case "Accessible washrooms":
        amenity_list.push(
            <span title={amenity}>♿</span>
        );
        break;
    }
  }

  return <div>{amenity_list}</div>;
}

function formatAmenitiesDetail(amenities) {
  let amenity_list = [];

  for (var i = 0; i < amenities.length; i++) {
    let amenity = amenities[i];

    switch(amenity) {
      case "Coastal Cafe":
        amenity_list.push(
            <div className="col-sm-3">🍔 {amenity}</div>
        );
        break;
      case "Pacific Buffet":
        amenity_list.push(
            <div className="col-sm-3">🍽️ {amenity}</div>
        );
        break;
      case "Coast Cafe Express":
      case "Arbutus Coffee Bar":
        amenity_list.push(
            <div className="col-sm-3">☕ {amenity}</div>
        );
        break;
      case "Pet Area":
        amenity_list.push(
            <div className="col-sm-3">🐕 {amenity}</div>
        );
        break;
      case "Seawest Lounge":
        amenity_list.push(
            <div className="col-sm-3">💺 {amenity}</div>
        );
        break;
      case "Passages Gift Shop":
      case "Passages":
        amenity_list.push(
            <div className="col-sm-3">🎁 {amenity}</div>
        );
        break;
      case "Kids Zone":
      case "Kids play areas":
        amenity_list.push(
            <div className="col-sm-3">🧒 {amenity}</div>
        );
        break;
      case "Video Zone":
        amenity_list.push(
            <div className="col-sm-3">🎮 {amenity}</div>
        );
        break;
      case "Work/study stations":
      case "Work stations":
        amenity_list.push(
            <div className="col-sm-3">💻 {amenity}</div>
        );
        break;
      case "Mobile charging stations":
        amenity_list.push(
            <div className="col-sm-3">🔌 {amenity}</div>
        );
        break;
      case "Accessible washrooms":
        amenity_list.push(
            <div className="col-sm-3">♿ {amenity}</div>
        );
        break;
    }
  }

  return <div className="row mb-4">{amenity_list}</div>;
}

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

export { getWaitColour, formatRibbon, formatDeparture, formatStatus, formatState, formatAmenities, formatAmenitiesDetail };
