import $ from 'jquery';
window.jQuery = $
window.$ = $
import 'bootstrap';
import './scss/app.scss';
import './ribbons.css';
import './footer.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import { Ferries } from "./components/Ferries";
import { ReallyAllSailings, AllSailings, RouteSailings, Sailing } from "./components/Sailings";
import { AllRoutes } from "./components/Routes";
import { Terminal, AllTerminals } from "./components/Terminals";

const Page404 = ({ location }) => (
  <div>
    <h1>Not found</h1>
    <p>Nothing here, sorry!</p>
  </div>
)

ReactDOM.render((
  <Router>
    <Switch>
      <Route exact path="/" component={AllRoutes}/>
      <Route exact path="/ferries" component={Ferries}/>
      <Route exact path="/routes" component={AllRoutes}/>
      <Route exact path="/sailings" component={AllSailings}/>
      <Route exact path="/all-sailings" component={ReallyAllSailings}/>
      <Route exact path="/terminals" component={AllTerminals}/>
      <Route path="/routes/:routeId" component={AllRoutes}/>
      <Route path="/sailings/route/:routeId" component={RouteSailings}/>
      <Route path="/sailings/:sailingId" component={Sailing}/>
      <Route path="/terminals/:terminalId" component={Terminal}/>
      <Route component={Page404} />
    </Switch>
  </Router>
), document.getElementById('app'))
