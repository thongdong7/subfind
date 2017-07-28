import React, { PropTypes } from "react";
import ReactDOM from "react-dom";
//import App from './App';
import "./index.css";

import { Router, Route, IndexRoute, hashHistory } from "react-router";

import AdminLTE from "./components/AdminLTE";

import SFConfigIndex from "./components/SFConfig/Index";
import SFReleaseList from "./components/SFRelease/List";

import toastr from "toastr";
import $ from "jquery";
import setup from "./setup";

// Import CSS
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap-theme.css";
import "toastr/build/toastr.css";
import "./index.css";
import "tb-react/index.css";
import { Provider } from "react-redux";
import thunk from "redux-thunk";

import { createStore, applyMiddleware } from "redux";
import reducers from "./reducers";

// Setup configuration
setup();

let store = createStore(reducers, applyMiddleware(thunk));

const Root = ({ store }) =>
  <Provider store={store}>
    <Router history={hashHistory}>
      <Route path="/" component={AdminLTE}>
        <IndexRoute component={SFReleaseList} />
        {/* <Route path="/release/config" component={SFConfigIndex} /> */}
        <Route path="/release/list" component={SFReleaseList} />
      </Route>
    </Router>
  </Provider>;

Root.propTypes = {
  store: PropTypes.object.isRequired,
};

ReactDOM.render(<Root store={store} />, document.getElementById("root"));
