import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { BasePage } from "./Base";
import { formatState, formatAmenitiesDetail, formatSailingTime, formatAverages } from "./Utils";
import { percentFullChart } from "./Charts";

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
          {formatSailingTime(data)}
          <div className="col-8 text-center p-0 pt-2 flex-column justify-content-center card card-block">
            {formatState(data)}
          </div>
        </div>
      </div>
      {formatAmenitiesDetail(data)}
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
