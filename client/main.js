// Generated file
'use strict';

import 'styles/main.scss';
import 'styles/switch.scss';
import 'toastr/toastr.scss';

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router'
// import Index from 'components/Index/Index';

// import App from 'components/App'
import AdminLTE from 'components/AdminLTE'

import SFConfigIndex from 'components/SFConfig/Index'
import SFReleaseList from 'components/SFRelease/List'

import toastr from 'toastr'

toastr.options.closeButton = true;
toastr.options.positionClass = "toast-top-left"

$(document).ajaxError(function() {
  toastr.error('Could not connect to subfind server')
});

render((
  <Router history={hashHistory}>
    <Route path="/" component={AdminLTE}>
      <IndexRoute component={SFReleaseList} />

      <Route path="/release/config" component={SFConfigIndex}/>
      <Route path="/release/list" component={SFReleaseList}/>

    </Route>
  </Router>
), document.getElementById('app'))
