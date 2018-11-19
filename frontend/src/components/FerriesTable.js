import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

var keys = ['name', 'status', 'last_updated'];
var headers = {
  'name': "Ferry",
  'status': "Status",
  'last_updated': "Last updated"
};

const FerriesTable = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        <strong>Ferries</strong>
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
FerriesTable.propTypes = {
  data: PropTypes.array.isRequired
};
export default FerriesTable;
