import React, {PropTypes} from 'react';
import ReactDOM from 'react-dom';
//import App from './App';
import './index.css';

import { Router, Route, IndexRoute, hashHistory } from 'react-router'

import AdminLTE from './components/AdminLTE'

//import SFConfigIndex from './components/SFConfig/Index'
import SFReleaseList from './components/SFRelease/List'

import toastr from 'toastr'
import $ from 'jquery'

toastr.options.closeButton = true;
toastr.options.positionClass = "toast-top-left"

$(document).ajaxError(function(e, response) {
  if (response.status === 0) {
    toastr.error('Could not connect to subfind server')
  }
});

import setup from './setup'

// Import CSS
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import 'toastr/build/toastr.css';
import './index.css';

// Setup configuration
setup()

import {createStore, Provider, middlewareAPI} from 'tb-react'

import actions from './actions'
const store = createStore(actions, middlewareAPI)

const Root = ({store}) => (
  <Provider store={store}>
    <Router history={hashHistory}>
      <Route path="/" component={AdminLTE}>
        <IndexRoute component={SFReleaseList} />


      </Route>
    </Router>
  </Provider>
);
//      <Route path="/release/config" component={SFConfigIndex}/>
//      <Route path="/release/list" component={SFReleaseList}/>

Root.propTypes = {
  store: PropTypes.object.isRequired,
};

ReactDOM.render(<Root store={store} />, document.getElementById('root'))
