import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import { AllSailings, RouteSailings, Sailing } from "./components/Sailings";
import { AllRoutes } from "./components/Routes";


ReactDOM.render((
  <Router>
    <Switch>
      <Route exact path="/" component={AllRoutes}/>
      <Route exact path="/routes" component={AllRoutes}/>
      <Route path="/routes/:routeId" component={AllRoutes}/>
      <Route exact path="/sailings" component={AllSailings}/>
      <Route path="/sailings/route/:routeId" component={RouteSailings}/>
      <Route path="/sailings/:sailingId" component={Sailing}/>
    </Switch>
  </Router>
), document.getElementById('app'))
