const path = require('path');

module.exports = {
  entry: './js/editor.js',  // your entry JavaScript file
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/js'),  // where the bundled file will be placed
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
  resolve: {
    alias: {
      editorjs: path.resolve(__dirname, 'node_modules/@editorjs/editorjs'),
    },
  },
};
