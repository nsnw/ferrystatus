import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { PercentFull } from "./PercentFull";
import { BasePage } from "./Base";
import { getWaitColour, formatAmenities, formatSailingTime } from "./Utils";

var moment = require('moment-timezone');

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
              {formatSailingTime(el.next_sailing)}
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
  <BasePage data={<AllRoutesTableInner data={data} />} />;

AllRoutesTable.propTypes = {
  data: PropTypes.array.isRequired
};

export { AllRoutesTable };
