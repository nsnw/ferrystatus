import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import { PercentFullLarge } from "./PercentFull";
import key from "weak-key";

function getDepartedStateColour(value) {
  let state = value;

  if (state == "Not departed")
    return "primary"
  else if (state == "Departed")
    return "danger"
  else
    return "success"
};

const SailingDetail = ({ data }) =>
  !data.route ? (
    <p>Sailing not found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>{data.scheduled_departure_hour_minute}</strong> sailing for <strong>{data.route}</strong>
      </h1>
      <h3 className="subtitle">
        <Link to="/sailings">
          <strong className="has-text-link">All sailings</strong>
        </Link> :&nbsp;
        <Link to={"/sailings/route/" + data.route_id}>
          Sailings for <strong className="has-text-link">{data.route}</strong>
        </Link>
      </h3>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Status</th>
            <th>Ferry</th>
            <th>Availability</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><h1 className="is-size-1"><strong className={"has-text-" + getDepartedStateColour(data.state)}>{data.state}</strong></h1></td>
            <td><h1 className="is-size-1"><strong>{data.ferry}</strong></h1></td>
            <td>{!data.percent_full ? ( <p></p> ) : ( <PercentFullLarge percentFull={data.percent_full} /> )}</td>
          </tr>
        </tbody>
      </table>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Time</th>
            <th>Event</th>
          </tr>
        </thead>
        <tbody>
          {data.events.map(ev => (
            <tr key={ev.timestamp}>
              <td>{ev.local_time}</td>
              <td>{ev.text}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
SailingDetail.propTypes = {
  data: PropTypes.object.isRequired
};
export default SailingDetail;
