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

function formatState(sailing) {
  if (sailing.state == "Arrived")
    return <div>
      <h1><strong>{sailing.state}</strong></h1>
      <h5>{sailing.eta_or_arrival_time_hour_minute}</h5>
    </div>
  else if (sailing.state == "Departed")
    return <div>
      <h1><strong>{sailing.state}</strong></h1>
      <h5>ETA {sailing.eta_or_arrival_time_hour_minute}</h5>
    </div>
  else
    return <div>
      <h1><strong>{sailing.state}</strong></h1>
      <h5>{sailing.status}</h5>
    </div>
};

function formatAverages(sailing) {
  // get averages
  let full = sailing.aggregates.percent_full;
  let leaving = sailing.aggregates.leaving;
  let arriving = sailing.aggregates.arriving;

  var full_content;
  var leaving_content;
  var arriving_content;

  let css_classes = "col-12 flex-column justify-content-center card card-block text-center m-1 h-100 ";

  if (full.average > 95)
    full_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-danger text-white"}>
      This sailing is normally <strong>full</strong> when it leaves
    </div></div>
  else if (full.average > 50)
    full_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-warning"}>
      This sailing normally <strong>has space</strong> when it leaves
    </div></div>
  else
    full_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-success text-white"}>
      This sailing is normally <strong>mostly empty</strong> when it leaves
    </div></div>

  if (leaving.average >= -5 && leaving.average <= 10)
    leaving_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-success text-white"}>
      This sailing normally leaves <strong>on time</strong>
    </div></div>
  else if (leaving.average < -5)
    leaving_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-warning"}>
      This sailing normally leaves <strong>early</strong>
    </div></div>
  else
    leaving_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-warning"}>
      This sailing normally leaves <strong>late</strong>
    </div></div>

  if (arriving.average >= -5 && arriving.average <= 10)
    arriving_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-success text-white"}>
      This sailing normally arrives <strong>on time</strong>
    </div></div>
  else if (arriving.average < -5)
    arriving_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-warning"}>
      This sailing normally arrives <strong>early</strong>
    </div></div>
  else
    arriving_content = <div className="col-12 col-lg-4"><div className={css_classes + "bg-warning"}>
      This sailing normally arrived <strong>late</strong>
    </div></div>

  return <div className="row col-12 p-1">
    {full_content}
    {leaving_content}
    {arriving_content}
  </div>
};


const SailingDetail = ({ data }) =>
  !data.route ? (
    <p>Sailing not found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>{data.route}</strong>
      </h1>
      <h3 className="subtitle">
        <Link to="/sailings">
          <strong className="has-text-link">All sailings</strong>
        </Link> :&nbsp;
        <Link to={"/sailings/route/" + data.route_id}>
          Sailings for <strong className="has-text-link">{data.route}</strong>
        </Link>
      </h3>
      <div className="row mb-4">
        <div className="row col-12">
          <div className="col-4 pt-2 bg-dark text-white text-center">
            <h2><strong className="text-white">{data.scheduled_departure_hour_minute}</strong></h2>
          </div>
          <div className="col-8 text-center p-0 flex-column justify-content-center card card-block">
            {formatState(data)}
          </div>
        </div>
      </div>
      {formatAverages(data)}
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Status</th>
            <th>Ferry</th>
            <th>Availability</th>
            {data.duration && <th>Duration</th> }
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><h1 className="is-size-2"><strong className={"has-text-" + getDepartedStateColour(data.state)}>{data.state}</strong></h1></td>
            <td><h1 className="is-size-2"><strong>{data.ferry}</strong></h1></td>
            <td>{!data.percent_full ? ( <p></p> ) : ( <PercentFullLarge percentFull={data.percent_full} /> )}</td>
            {data.duration && <td><h1 className="is-size-2">{data.duration} min</h1></td> }
          </tr>
        </tbody>
      </table>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Average full</th>
            <th>Average early/late leaving</th>
            <th>Average early/late arriving</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><h1 className="is-size-3">{data.aggregates.percent_full.average}%</h1></td>
            <td><h1 className="is-size-3">{data.aggregates.leaving.average} min</h1></td>
            <td><h1 className="is-size-3">{data.aggregates.arriving.average} min</h1></td>
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
