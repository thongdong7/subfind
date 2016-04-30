'use strict';

var webpack = require('webpack');
var config = require('./webpack.config.base.js');

if (process.env.NODE_ENV !== 'test') {
  config.entry = [
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/dev-server'
  ].concat(config.entry);
}

config.devtool = 'cheap-module-eval-source-map';

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin()
]);

config.module.loaders = config.module.loaders.concat([
  {test: /\.jsx?$/, loader: 'react-hot!babel-loader?presets[]=react,presets[]=es2015,presets[]=stage-0',
      exclude: /node_modules/}
]);

module.exports = config;
