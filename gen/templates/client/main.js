// Generated file
'use strict';

import 'styles/main.scss';
{% for item in components -%}
  {%- if item.css -%}
  {%- for css in item.css -%}
import '{{css}}'
  {%- endfor %}
  {%- endif %}
{%- endfor %}

// Extra components
{%- for item in extraComponents -%}
  {%- if item.css and item.webpackImport -%}
  {%- for css in item.css %}
import '{{css}}'
  {%- endfor %}
  {%- endif %}
{%- endfor %}

import React from 'react';
import { render } from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router'

import AdminLTE from 'components/AdminLTE'

import SFConfigIndex from 'components/SFConfig/Index'
import SFReleaseList from 'components/SFRelease/List'

import toastr from 'toastr'

toastr.options.closeButton = true;
toastr.options.positionClass = "toast-top-left"

$(document).ajaxError(function(e, response) {
  if (response.status == 0) {
    toastr.error('Could not connect to subfind server')
  }

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
