import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

var keys = ['route', 'scheduled_departure', 'state', 'ferry'];
var headers = {
  'route': "Route",
  'scheduled_departure': "Scheduled departure",
  'state': "Status",
  'ferry': "Ferry"
};

const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        <strong>Sailings</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            {Object.entries(data[0]).filter(el => keys.includes(el[0])).map(el => <th key={key(el)}>{headers[el[0]]}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              {Object.entries(el).filter(el => keys.includes(el[0])).map(el => <td key={key(el)}>{el[1]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
Table.propTypes = {
  data: PropTypes.array.isRequired
};
export default Table;
