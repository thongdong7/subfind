'use strict';

var webpack = require('webpack');
var config = require('./webpack.config.base.js');

var SaveAssetsJson = require('assets-webpack-plugin');

config.bail = true;
config.debug = false;
config.profile = false;
config.devtool = '#source-map';

config.output = {
  path: './client/dist',
  pathInfo: true,
  publicPath: '/js/',
  filename: 'bundle.js'
};

config.entry = {
  vendor: [
    'admin-lte/bootstrap/css/bootstrap.css',
    'font-awesome/css/font-awesome.min.css',
    'ionicons/dist/css/ionicons.min.css',
    'admin-lte/dist/css/AdminLTE.min.css',
    'admin-lte/dist/css/skins/skin-blue.min.css',
    'jquery',
    'admin-lte/bootstrap/js/bootstrap.js',
    'admin-lte/dist/js/app.js',
    'lodash',
    'babel-polyfill',
    'react',
    'react-addons-update',
    'react-router',
    'react-typeahead',

    'react-dom'
  ],
  app: "./client/main.js",
}

//config.output = {
//
//}

config.plugins = config.plugins.concat([
  new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
  }),
  new webpack.optimize.OccurenceOrderPlugin(true),
  new webpack.optimize.DedupePlugin(),

//  new webpack.optimize.UglifyJsPlugin({
//    output: {
//      comments: false
//    },
//    compress: {
//      warnings: false,
//      screw_ie8: true
//    }
//  }),
  new webpack.optimize.CommonsChunkPlugin(/* chunkName= */"vendor", /* filename= */"vendor.bundle.js"),
//  new SaveAssetsJson({
//    path: process.cwd(),
//    filename: 'assets.json'
//  }),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('production')
    }
  })
]);

config.module.loaders = config.module.loaders.concat([
  {test: /\.jsx?$/, loader: 'babel?presets[]=react,presets[]=es2015,presets[]=stage-0', exclude: /node_modules/},
  { test: /\.css$/, loader: "style-loader!css-loader" },
  { test: /\.woff/, loader: "file-loader" },
  { test: /\.eot/, loader: "file-loader" },
  { test: /\.ttf/, loader: "file-loader" },
  { test: /\.svg/, loader: "file-loader" },
  { test: /\.jpg/, loader: "file-loader" },
]);

module.exports = config;
