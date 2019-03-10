import React from "react";
import { Link } from "react-router-dom";
import DataProvider from "./DataProvider";
import PropTypes from "prop-types";
import { BasePage } from "./Base";

const TerminalCardsInner = ({ data }) =>
  !data.length ? (
    <p>No routes found</p>
  ) : (
    <div className="column">
      <h1 className="title">
        <strong>Terminals</strong>
      </h1>
      <p></p>
      <div className="row mb-4 m-0 terminals">
        {data.map(el => (
          <div key={el.id} className="col-12 col-lg-6 p-1">
            <div className="col-12 text-center bg-primary p-1">
              <h5 className="mb-0"><strong className="text-white">{el.name}</strong></h5>
            </div>
            <div className="col-12 p-2 pt-0 text-center flex-column justify-content-center card card-block">
              <div className="col-12">
              {el.routes.map(route => (
                <div key={route.id} className="col-12">
                  <Link to={`/sailings/route/${route.id}`}>{route.name}</Link>
                </div>
              ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

const TerminalCards = ({ data }) =>
  <BasePage data={<TerminalCardsInner data={data} />} />

TerminalCards.propTypes = {
  data: PropTypes.array.isRequired
};

const AllTerminals = (props) => (
  <DataProvider endpoint="/api/terminals"
                render={data => <TerminalCards data={data.response} />} />
);

const Terminal = (props) => (
  <DataProvider endpoint="/api/terminals"
                render={data => <TerminalCards data={data.response} />} />
);

export { Terminal, AllTerminals }
