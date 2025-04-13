const path = require('path');
const webpack = require('webpack');

module.exports = {
  resolve: {
    alias: {
      'process/browser': 'process/browser.js'  // 👈 Force exact match
    },
    fallback: {
      stream: require.resolve('stream-browserify'),
      assert: require.resolve('assert'),
      url: require.resolve('url/'),
      zlib: require.resolve('browserify-zlib'),
      http: require.resolve('stream-http'),
      https: require.resolve('https-browserify'),
      process: require.resolve('process/browser.js'),
    },
  },
  plugins: [
    new webpack.ProvidePlugin({
      process: 'process/browser.js',
      Buffer: ['buffer', 'Buffer'],
    }),
  ],
};
