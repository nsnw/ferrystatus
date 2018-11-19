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
  <progress class={"progress is-" + getPercentFullColour(percentFull)} value={percentFull} max="100">{percentFull + "%"}</progress>

PercentFull.propTypes = {
  percentFull: PropTypes.number.isRequired
};
export default PercentFull
