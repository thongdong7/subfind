'use strict';

import 'styles/main.scss';

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router'
import Index from 'components/Index/Index';

import App from 'components/App'
import AdminLTE from 'components/AdminLTE'


import CoffeeAreaCreate from 'components/CoffeeArea/Create'
import CoffeeAreaUpdate from 'components/CoffeeArea/Update'
import CoffeeAreaList from 'components/CoffeeArea/List'

import CoffeeTableCreate from 'components/CoffeeTable/Create'
import CoffeeTableUpdate from 'components/CoffeeTable/Update'
import CoffeeTableList from 'components/CoffeeTable/List'

import CoffeeProductCreate from 'components/CoffeeProduct/Create'
import CoffeeProductUpdate from 'components/CoffeeProduct/Update'
import CoffeeProductList from 'components/CoffeeProduct/List'

import CoffeeOrderCreate from 'components/CoffeeOrder/Create'
import CoffeeOrderUpdate from 'components/CoffeeOrder/Update'
import CoffeeOrderList from 'components/CoffeeOrder/List'

import SFConfigIndex from 'components/SFConfig/Index'
import SFReleaseList from 'components/SFRelease/List'

render((
  <Router history={hashHistory}>
    <Route path="/" component={AdminLTE}>
      <IndexRoute component={SFReleaseList} />

      <Route path="/release/config" component={SFConfigIndex}/>
      <Route path="/release/list" component={SFReleaseList}/>

      <Route path="/coffee-area/list" component={CoffeeAreaList}/>
      <Route path="/coffee-area/create" component={CoffeeAreaCreate}/>
      <Route path="/coffee-area/:id" component={CoffeeAreaUpdate}/>

      <Route path="/coffee-table/list" component={CoffeeTableList}/>
      <Route path="/coffee-table/create" component={CoffeeTableCreate}/>
      <Route path="/coffee-table/:id" component={CoffeeTableUpdate}/>

      <Route path="/coffee-product/list" component={CoffeeProductList}/>
      <Route path="/coffee-product/create" component={CoffeeProductCreate}/>
      <Route path="/coffee-product/:id" component={CoffeeProductUpdate}/>

      <Route path="/coffee-order/list" component={CoffeeOrderList}/>
      <Route path="/coffee-order/create" component={CoffeeOrderCreate}/>
      <Route path="/coffee-order/:id" component={CoffeeOrderUpdate}/>


    </Route>
  </Router>
), document.getElementById('app'))
