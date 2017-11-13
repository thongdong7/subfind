import React from "react";
import ReactDOM from "react-dom";
import "./index.css";

import { HashRouter as Router, Route, Switch } from "react-router-dom";

import SFReleaseList from "./components/SFRelease/List";
import SFConfigIndex from "./components/SFConfig/Index";

// Import CSS
import "./index.css";
import { Provider } from "react-redux";
import thunk from "redux-thunk";

import { createStore, applyMiddleware } from "redux";
import reducers from "./reducers";

// Setup configuration
let store = createStore(reducers, applyMiddleware(thunk));

// Subscribe
var source = new EventSource("http://localhost:32500/subscribe");
source.onmessage = function(event) {
  try {
    const action = JSON.parse(event.data);

    store.dispatch(action);
  } catch (e) {
    console.error(e);
  }
};

const Root = ({ store }) => (
  <Provider store={store}>
    <Router>
      <Switch>
        <Route exact path="/config" component={SFConfigIndex} />
        <Route exact path="/" component={SFReleaseList} />
        {/* <Route path="/release/config" component={SFConfigIndex} /> */}
      </Switch>
    </Router>
  </Provider>
);

ReactDOM.render(<Root store={store} />, document.getElementById("root"));
