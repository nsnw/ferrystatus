import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import { PercentFull } from "./PercentFull";
import key from "weak-key";
import { BasePage } from "./Base";
import { formatState, formatAmenitiesDetail } from "./Utils";
import { percentFullChart } from "./Charts";

function getDepartedStateColour(value) {
  let state = value;

  if (state == "Not departed")
    return "primary"
  else if (state == "Departed")
    return "danger"
  else
    return "success"
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
    </div></div>
  else if (full.average > 50)
    full_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-warning"}>
      <p>This sailing normally <strong>at least half full</strong> when it leaves</p>
    </div></div>
  else
    full_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing is normally <strong>mostly empty</strong> when it leaves</p>
    </div></div>

  if (leaving.average >= -5 && leaving.average <= 10)
    leaving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally leaves <strong>on time</strong></p>
    </div></div>
  else if (leaving.average < -5)
    leaving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally leaves <strong>early</strong></p>
    </div></div>
  else
    leaving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-warning"}>
      <p>This sailing normally leaves <strong>late</strong></p>
    </div></div>

  if (arriving.average >= -5 && arriving.average <= 10)
    arriving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally arrives <strong>on time</strong></p>
    </div></div>
  else if (arriving.average < -5)
    arriving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-success text-white"}>
      <p>This sailing normally arrives <strong>early</strong></p>
    </div></div>
  else
    arriving_content = <div className="col-12 col-lg-4 mb-1"><div className={css_classes + "bg-warning"}>
      <p>This sailing normally arrives <strong>late</strong></p>
    </div></div>

  return <div className="row col-12 p-1">
    {full_content}
    {leaving_content}
    {arriving_content}
  </div>
}


const SailingDetailInner = ({ data }) =>
  !data.route ? (
    <p>Sailing not found</p>
  ) : (
    <div className="column">
      <div className="row mb-4 mt-4">
        <h3 className="title">
          <strong>{data.route}</strong>
        </h3>
      </div>
      <div className="row mb-4">
        <div className="row col-12 m-0 p-0">
          <div className="col-4 pt-2 bg-dark text-white text-center">
            <h2><strong className="text-white">{data.scheduled_departure_hour_minute}</strong></h2>
          </div>
          <div className="col-8 text-center p-0 pt-2 flex-column justify-content-center card card-block">
            {formatState(data)}
          </div>
        </div>
      </div>
      {formatAmenitiesDetail(data.ferry.amenities)}
      {formatAverages(data)}
      {percentFullChart(data.percent_full_data)}
      {!data.events ? ( <p></p> ) : (
        <div className="row card mb-5 mt-5">
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
      )}
      <div className="row justify-content-between mb-5">
        <div className="col-6 text-left">
            <Link className="btn btn-primary" to="/routes">
              <strong className="has-text-link">↩ All routes</strong>
            </Link>
        </div>
        <div className="col-6 text-right">
            <Link className="btn btn-primary" to={"/sailings/route/" + data.route_id}>
              <strong className="has-text-link">This route ↪</strong>
            </Link>
        </div>
      </div>
    </div>
  );

const SailingDetail = ({ data }) =>
  <BasePage data={<SailingDetailInner data={data} />} />

SailingDetail.propTypes = {
  data: PropTypes.object.isRequired
};
export default SailingDetail;
