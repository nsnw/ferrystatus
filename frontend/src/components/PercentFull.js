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
  <progress className={"progress is-" + getPercentFullColour(percentFull)} value={percentFull} max="100">{percentFull + "%"}</progress>

PercentFull.propTypes = {
  percentFull: PropTypes.number.isRequired
};

const PercentFullLarge = ({ percentFull }) =>
  <h1 className="is-size-1"><strong className={"has-text-" + getPercentFullColour(percentFull)}>{percentFull + "%"}</strong></h1>

PercentFullLarge.propTypes = {
  percentFull: PropTypes.number.isRequired
};
export { PercentFull, PercentFullLarge }
