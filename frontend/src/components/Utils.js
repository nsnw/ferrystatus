import React from "react";
import { PercentFull } from "./PercentFull";
import {Link} from "react-router-dom";

var moment = require('moment-timezone');

function formatState(sailing) {
  let ferry_name = sailing.ferry ? sailing.ferry.name : undefined;

  if (sailing.state === "Arrived")
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong>{sailing.state}</strong> at {sailing.eta_or_arrival_time_hour_minute}</h1>
      <div className="p-2"><PercentFull percentFull={sailing.percent_full} /></div>
    </div>;
  else if (sailing.state === "Departed")
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong>{sailing.state}</strong> at {sailing.actual_departure_hour_minute}</h1>
    </div>;
  else if (sailing.status === "Cancelled")
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong className="rounded p-1 pl-2 pr-2 text-white bg-danger">Cancelled</strong></h1>
    </div>;
  else
    return <div>
      <h5>{ferry_name}</h5>
      <h1><strong>{sailing.state}</strong></h1>
      <h5>{sailing.status}</h5>
    </div>;
}

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

function formatAmenitiesDetail(sailing) {
  if (sailing.ferry) {
    let amenities = sailing.ferry.amenities;
    let amenity_list = [];

    for (var i = 0; i < amenities.length; i++) {
      let amenity = amenities[i];

      switch (amenity) {
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

    return <div className="row mb-4 p-2 sailingAmenities">{amenity_list}</div>;
  } else {
    return;
  }
}

function getDepartedStateColour(value) {
  let state = value;

  if (state === "Not departed")
    return "primary";
  else if (state === "Departed")
    return "danger";
  else
    return "success"
}

function getWaitColour(value) {
  let waits = value;

  if (waits === 0)
    return "success";
  else if (waits === 1 )
    return "warning";
  else if (waits > 1 )
    return "danger";
  else
    return "secondary"
}

function formatRibbon(sailing) {

  let ts = moment(new Date(sailing.scheduled_departure*1000)).tz("America/Vancouver");
  let now = moment().tz("America/Vancouver");

  if (sailing.status === "Cancelled")
    return <div className="corner-ribbon red">Cancelled</div>;
  else if (sailing.status && sailing.status !== "On Time")
    return <div className="corner-ribbon turquoise">Delayed</div>;
  else if (sailing.percent_full > 90)
    return <div className="corner-ribbon orange">{sailing.percent_full}% full</div>;
  else if (ts.date() !== now.date())
    return <div className="corner-ribbon purple">Tomorrow</div>;
  else
    return <div className="corner-ribbon green">On time</div>;

}

function formatDeparture(sailing) {
  var state;

  state = <span className="align-middle">{sailing.scheduled_departure_hour_minute}</span>;
  return state;
}

function formatStatus(sailing) {
  let cssStatus = getDepartedStateColour(sailing.state);
  var state;

  if (sailing.state === "Departed")
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>({sailing.eta_or_arrival_time_hour_minute})</i></span>;
  else if (sailing.state === "Arrived")
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong> <i>({sailing.eta_or_arrival_time_hour_minute})</i></span>;
  else
    state = <span><strong className={"has-text-" + cssStatus}>{sailing.state}</strong></span>;
  
  return state;
}

function formatStatusText(sailing) {
  if (sailing.state === "Not departed" && sailing.status !== "Cancelled" && sailing.status && sailing.status !== "On Time")
    return <td colSpan="5"><small> → {sailing.status}</small></td>;
}

function formatSailingTime(sailing) {
  // Build the date/time component, along with the status ribbon
  return <div className="col-4 pt-2 pl-1 pb-3 bg-dark text-white text-center">
    {formatRibbon(sailing)}
    {sailing.local_date}
    <Link to={`/sailings/${sailing.id}`}>
      <h2><strong className="text-white">{formatDeparture(sailing)}</strong></h2>
    </Link>
  </div>;
}

function formatAverages(sailing) {
  // get averages
  let full = sailing.aggregates.percent_full;
  let leaving = sailing.aggregates.leaving;
  let arriving = sailing.aggregates.arriving;

  var full_content;
  var leaving_content;
  var arriving_content;

  let css_classes = "col-12 flex-column justify-content-center card card-block text-center m-1 h-100 align-middle ";

  if (full.average > 95)
    full_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-danger text-white"}>
      <p>This sailing is normally <strong>full</strong> when it leaves</p>
    </div></div>;
  else if (full.average > 50)
    full_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-warning"}>
      <p>This sailing normally <strong>at least half full</strong> when it leaves</p>
    </div></div>;
  else
    full_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing is normally <strong>mostly empty</strong> when it leaves</p>
    </div></div>;

  if (leaving.average >= -5 && leaving.average <= 10)
    leaving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally leaves <strong>on time</strong></p>
    </div></div>;
  else if (leaving.average < -5)
    leaving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally leaves <strong>early</strong></p>
    </div></div>;
  else
    leaving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-warning"}>
      <p>This sailing normally leaves <strong>late</strong></p>
    </div></div>;

  if (arriving.average >= -5 && arriving.average <= 10)
    arriving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally arrives <strong>on time</strong></p>
    </div></div>;
  else if (arriving.average < -5)
    arriving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally arrives <strong>early</strong></p>
    </div></div>;
  else
    arriving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-warning"}>
      <p>This sailing normally arrives <strong>late</strong></p>
    </div></div>;

  return <div className="row col-12 p-1 m-0 pb-4 sailingAverages">
    {full_content}
    {leaving_content}
    {arriving_content}
  </div>
}

export { getWaitColour, formatRibbon, formatDeparture, formatStatus, formatState, formatAmenities,
  formatAmenitiesDetail, formatSailingTime, getDepartedStateColour, formatStatusText, formatAverages
};
