import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";


const BasePage = ({ data }) =>
  <>
  <nav className="navbar navbar-default navbar-expand-lg navbar-dark bg-primary" role="navigation" aria-label="main navigation">
    <Link className="navbar-brand" to="/">
      <b>⛴ FerryStatus</b>
    </Link>

    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarSupportedContent">
      <ul className="navbar-nav mr-auto">
        <li className="nav-item active">
          <Link className="nav-link" to="/routes">
          Routes
          </Link>
        </li>
        <li className="nav-item active">
          <Link className="nav-link" to="/terminals">
          Terminals
          </Link>
        </li>
        <li className="nav-item active">
          <Link className="nav-link" to="/ferries">
          Ferries
          </Link>
        </li>
        <li className="nav-item active">
          <Link className="nav-link" to="/about">
          About
          </Link>
        </li>
        <li className="nav-item active">
          <Link className="nav-link" to="/faq">
          FAQ
          </Link>
        </li>
        <li className="nav-item active">
          <Link className="nav-link" to="/privacy">
          Privacy
          </Link>
        </li>
      </ul>
    </div>
  </nav>
  <div className="pb-2">
    <section className="section pl-3 pt-3">
      <div className="container">
        <div className="columns">{data}</div>
      </div>
    </section>
  </div>
  </>

export { BasePage };
