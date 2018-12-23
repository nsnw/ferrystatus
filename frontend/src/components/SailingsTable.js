import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PropTypes from "prop-types";
import key from "weak-key";
import { PercentFull } from "./PercentFull"
import { getWaitColour, formatDeparture, formatStatus, formatRibbon, formatState } from "./Utils"

function formatStatusText(sailing) {
  if (sailing.state == "Not departed" && sailing.status != "Cancelled" && sailing.status && sailing.status != "On Time")
    return <td colSpan="5"><small> → {sailing.status}</small></td>
};

const AllSailingsTable = ({ data }) =>
  !data.length ? (
    <p>No sailings found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>All sailings</strong>
      </h1>
      {data.map(el => (
        <div key={el.id} className="row mb-4">
          <div className="col-12 row pr-0">
            <div className="col-12 p-1 pl-3 pt-2 bg-primary">
              <Link to={`/sailings/${el.id}`}>
                <strong className="text-white">{el.route}</strong>
              </Link>
            </div>
          </div>
          <div className="row col-12 pr-0">
            <div className="col-12 row pr-0">
              <div className="col-4 pt-2 bg-dark text-white text-center">
                <Link to={`/sailings/${el.id}`}>
                  <h2><strong className="text-white">{el.scheduled_departure_hour_minute}</strong></h2>
                </Link>
              </div>
            </div>
          </div>
          <div className="col-3">{formatDeparture(el)}</div>
          <div className="col-3">{formatStatus(el)}</div>
          <div className="col-6"><strong>{el.ferry}&nbsp;</strong></div>
          <div className="col-6">{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</div>
        </div>
      ))}
    </div>
  );
AllSailingsTable.propTypes = {
  data: PropTypes.array.isRequired
};

const RouteSailingsTable = ({ data }) =>
  !data.sailings ? (
    <p>No sailings found</p>
  ) : (
    <div className="row mb-4">
      <div className="col-12 row p-0 m-0">
        <div className="col-10 p-1 pl-3 pt-2 bg-primary">
          <strong className="text-white">{data.route.name}</strong>
        </div>
        <div className="col-2 row p-0 mr-0">
          <div className={"col-6 text-center p-0 pt-1 bg-" + getWaitColour(data.route.car_waits)}>🚗</div>
          <div className={"col-6 text-center p-0 pt-1 bg-" + getWaitColour(data.route.oversize_waits)}>🚚</div>
        </div>
      </div>
      {data.sailings.map(el => (
        <div key={el.id} className="row col-12 p-0 m-0 pb-1">
          <div className="col-12 row p-0 m-0">
            <div className="col-4 pt-2 pl-1 bg-dark text-white text-center">
              {formatRibbon(el)}
              <Link to={`/sailings/${el.id}`}>
                <h2><strong className="text-white">{formatDeparture(el)}</strong></h2>
              </Link>
            </div>
            <div className="col-8 row pr-0">
              <div className="col-lg-8 col-12 text-center p-0 pt-1 flex-column justify-content-center card card-block">
                <h5>
                  {!el.ferry ? ( <strong className="text-black-50">TBC</strong> ) : ( <strong>{el.ferry}</strong> )}
                </h5>
                {formatStatusText(el)}
              </div>
              <div className="col-lg-4 col-12 p-2 flex-column justify-content-center card card-block">{!el.percent_full ? ( <p></p> ) : ( <PercentFull percentFull={el.percent_full} /> )}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
RouteSailingsTable.propTypes = {
  data: PropTypes.object.isRequired
};
export { RouteSailingsTable, AllSailingsTable };

