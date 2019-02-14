import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { BasePage } from "./Base";

const FAQPage = () =>
  <BasePage data={
    <>
      <h1 className="title">Frequently Asked Questions</h1>
      <h2><strong>Where does the information on this site come from?</strong></h2>
      <p>
      All of the information contained on this site is taken from the BC Ferries website - in particular:-
      <ul>
        <li> <a href="https://www.bcferries.com/current_conditions/actualDepartures.html">Departures and Arrivals</a></li>
        <li> <a href="https://www.bcferries.com/current_conditions/terminals.html">Terminals at a Glance</a></li>
        <li> <a href="https://www.bcferries.com/current_conditions/vessel_positions.html">Vessel positions</a></li>
      </ul>
      </p>
      <h2><strong>The route I'm looking for is missing!</strong></h2>
      <p>
      Unfortunately, BC Ferries doesn't provide live information for all routes. The information they do provide is limited to the major routes between south Vancouver Island, some of the Gulf Islands and the mainland.
      </p>
      <h2><strong>I've found a bug, what do I do?</strong></h2>
      <p>
      Let me know! Either <a href="https://github.com/ve7cxz/ferrystatus/issues/new">create an issue on GitHub</a> or drop me an email (to <a href="mailto:andy@nsnw.ca">andy@nsnw.ca</a>) with the details and I'll take a look!
      </p>
      <h2><strong>I've had an idea!</strong></h2>
      <p>
      Again, let me know - either via GitHub or via email to the same address above! I can't promise anything, as this is something I work on in my spare time, but if it's a good idea I'll see what I can do.
      </p>
      <h2><strong>Technical details! Hit me!</strong></h2>
      <p>
      This site is built using <a href="https://www.djangoproject.com/">Django</a> (which is a Python web framework) and the front-end uses <a href="https://reactjs.org/">React</a> to dynamically generate the information pages. The process that retrieves the data from the BC Ferries website is also written in Python and makes heavy use of <a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>, which is indispensible for parsing other web pages. The backend database in use is <a href="https://www.postgresql.org/">PostgreSQL</a>, and the whole thing is running in <a href="https://www.docker.com/">Docker</a> containers, using <a href="http://dokku.viewdocs.io/dokku/">Dokku</a> to simplify deployment
      </p>
      <p>
      There is an API of sorts (which you can see if you poke around under the hood), but it's by no means guaranteed to be stable.
      </p>
      <p>
      The source code can be found on <a href="https://github.com/ve7cxz/ferrystatus">GitHub</a> under an <a href="https://opensource.org/licenses/MIT">MIT</a> license.
      </p>
    </>
  } />

const AboutPage = () =>
  <BasePage data={
    <>
      <h1 class="title">About this site</h1>
      <h2><strong>First of all, some important information...</strong></h2>
      <p>
      This site is in no way affiliated, supported or endorsed by BC Ferries. The data provided here is purely for informational purposes, and is not an official representation of BC Ferries' schedules. To view the official schedules and current conditions for all BC Ferries routes, click <a href="https://www.bcferries.com/current_conditions/">here</a>.
      </p>
      <h2><strong>So what is this?</strong></h2>
      <p>
      I made this in my spare time as a way to learn a few things, and also to present information on something that I - as a resident of Victoria - find useful, and in a clean, readable way.
      </p>
      <p>
      I also thought it might be interesting to see if it's possible to generate useful statistics about things such as how quickly sailings fill up, or which sailings are more likely to be late.
      </p>
      <h2><strong>Contacting me</strong></h2>
      <p>You can contact me by e-mail at <a href="mailto:andy@nsnw.ca">andy@nsnw.ca</a>, or you can find me on Twitter as <a href="https://twitter.com/ve7cxz">@ve7cxz</a>.
      </p>
    </>
  } />

const PrivacyPage = () =>
  <BasePage data={
    <>
      <h1 class="title">Privacy policy</h1>
      <h2><strong>What data does this site collect?</strong></h2>
      <p>
      This site does not intentionally collect any data about users. However, as is standard practice for websites, the following information is logged for each request:-
      <ul>
        <li>the user's IP address</li>
        <li>the user's browser's <a href="https://en.wikipedia.org/wiki/User_agent">User agent</a> information</li>
        <li>the page the user requested</li>
      </ul>
      This information is retained solely for diagnostic and security purposes, and is automatically deleted after a few weeks. No attempts are made to associate this information with an individual.
      </p>
      <h2><strong>What cookies does this site use?</strong></h2>
      <p>
      This site may set cookies to store state for certain parts of the site. These are used to store user settings.
      </p>
      <p>
      This site does not make use of any 3rd-party cookies.
      </p>
      <h2><strong>What tracking or analytics does this site use?</strong></h2>
      <p>
      At the moment, this site does not perform any analytics either in-browser or on the server side. If this changes, it will be clearly communicated on the front page of this site
      </p>
    </>
  } />

export { AboutPage, FAQPage, PrivacyPage };
