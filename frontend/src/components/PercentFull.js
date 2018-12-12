import React from "react";
import PropTypes from "prop-types";

function getPercentFullColour(value) {
  let percent_full = value;

  if (percent_full > 90)
    return "danger";
  else if (percent_full > 70)
    return "warning";
  else
    return "success";
}


const PercentFull = ({ percentFull }) =>
  <div className="progress">
    <div className={"progress-bar bg-" + getPercentFullColour(percentFull)} role="progressbar" style={{width: percentFull + "%"}} aria-valuenow={percentFull} aria-valuemin="0" aria-valuemax="100"></div>
  </div>

PercentFull.propTypes = {
  percentFull: PropTypes.number.isRequired
};

const PercentFullLarge = ({ percentFull }) =>
  <h1 className="is-size-2"><strong className={"has-text-" + getPercentFullColour(percentFull)}>{percentFull + "%"}</strong></h1>

PercentFullLarge.propTypes = {
  percentFull: PropTypes.number.isRequired
};
export { PercentFull, PercentFullLarge }
