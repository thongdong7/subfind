// Generated file
'use strict';

import 'styles/main.scss';
import 'styles/switch.scss';

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router'
// import Index from 'components/Index/Index';

// import App from 'components/App'
import AdminLTE from 'components/AdminLTE'


// import CoffeeAreaCreate from 'components/CoffeeArea/Create'
// import CoffeeAreaUpdate from 'components/CoffeeArea/Update'
// import CoffeeAreaList from 'components/CoffeeArea/List'
//
// import CoffeeTableCreate from 'components/CoffeeTable/Create'
// import CoffeeTableUpdate from 'components/CoffeeTable/Update'
// import CoffeeTableList from 'components/CoffeeTable/List'
//
// import CoffeeProductCreate from 'components/CoffeeProduct/Create'
// import CoffeeProductUpdate from 'components/CoffeeProduct/Update'
// import CoffeeProductList from 'components/CoffeeProduct/List'
//
// import CoffeeOrderCreate from 'components/CoffeeOrder/Create'
// import CoffeeOrderUpdate from 'components/CoffeeOrder/Update'
// import CoffeeOrderList from 'components/CoffeeOrder/List'

import SFConfigIndex from 'components/SFConfig/Index'
import SFReleaseList from 'components/SFRelease/List'

render((
  <Router history={hashHistory}>
    <Route path="/" component={AdminLTE}>
      <IndexRoute component={SFReleaseList} />

      <Route path="/release/config" component={SFConfigIndex}/>
      <Route path="/release/list" component={SFReleaseList}/>

    </Route>
  </Router>
), document.getElementById('app'))