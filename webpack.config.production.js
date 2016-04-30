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
    'jquery',
    'babel-polyfill',
    'react',
    'react-addons-update',
    'react-router',
    'react-typeahead'
  ],
  app: "./client/main.js",
}

//config.output = {
//
//}

config.plugins = config.plugins.concat([
  new webpack.optimize.OccurenceOrderPlugin(true),
  new webpack.optimize.DedupePlugin(),
  new webpack.optimize.CommonsChunkPlugin(/* chunkName= */"vendor", /* filename= */"vendor.bundle.js"),
//  new webpack.optimize.UglifyJsPlugin({
//    output: {
//      comments: false
//    },
//    compress: {
//      warnings: false,
//      screw_ie8: true
//    }
//  }),
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
  {test: /\.jsx?$/, loader: 'babel?presets[]=react,presets[]=es2015,presets[]=stage-0', exclude: /node_modules/}
]);

module.exports = config;
