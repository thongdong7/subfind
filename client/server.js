'use strict';

import 'styles/main.scss';

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router'
import Index from 'components/Index/Index';

import App from 'components/App'
import AdminLTE from 'components/AdminLTE'


import CoffeeTableCreate from 'components/CoffeeTable/Create'
import CoffeeTableleUpdate from 'components/CoffeeTable/Update'
import CoffeeTableList from 'components/CoffeeTable/List'

import CoffeeAreaCreate from 'components/CoffeeArea/Create'
import CoffeeArealeUpdate from 'components/CoffeeArea/Update'
import CoffeeAreaList from 'components/CoffeeArea/List'


render((
  <Router history={hashHistory}>
    <Route path="/" component={AdminLTE}>
      <IndexRoute component={App} />

      
      <Route path="/coffee-table/list" component={CoffeeTableList}/>
      <Route path="/coffee-table/create" component={CoffeeTableCreate}/>
      <Route path="/coffee-table/:id" component={CoffeeTableUpdate}/>
      
      <Route path="/coffee-area/list" component={CoffeeAreaList}/>
      <Route path="/coffee-area/create" component={CoffeeAreaCreate}/>
      <Route path="/coffee-area/:id" component={CoffeeAreaUpdate}/>
      

    </Route>
  </Router>
), document.getElementById('app'))