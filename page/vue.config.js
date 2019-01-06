const path = require('path')
const webpack = require('webpack')

module.exports = {
    pwa: {
        workboxOptions: {
            templatedUrls: {
                '/': 'index.ssr.html'
            }
        }
    },
    configureWebpack: {
        plugins: [
            new webpack.ProvidePlugin({
                '_': path.resolve(__dirname, './src/lodash.js')
            }),
            new webpack.ProvidePlugin({
                '$': path.resolve(__dirname, './src/tools.js')
            })
        ]
    }
}
