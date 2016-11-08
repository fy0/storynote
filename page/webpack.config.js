var path = require('path')
var webpack = require('webpack')

module.exports = {
    entry: './src/main.js',
    output: {
        path: path.resolve(__dirname, './dist'),
        publicPath: '/dist/',
        filename: 'build.js'
    },
    resolveLoader: {
        root: path.join(__dirname, 'node_modules'),
    },
    module: {
        loaders: [
            {
                test: /\.vue$/,
                loader: 'vue'
            },
            {
                test: /\.js$/,
                loader: 'babel',
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                loader: 'style!css!postcss',
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'url-loader?limit=8192',
                query: {
                    name: '[name].[ext]?[hash]'
                }
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                loader: 'url-loader?limit=65000&name=fonts/[name]_[hash].[ext]'
            },
        ]
    },
    babel: {
        presets: ['es2015', 'stage-2'],
        plugins: ['transform-runtime'],
        compact: false,
        cacheDirectory: true, //important for performance
    },
    postcss: function () {
        return [require('autoprefixer'), require('precss')];
    },
    resolve: {
        alias: {
            cash: path.join(__dirname, 'node_modules/cash-dom/dist/cash.js'),
        },
        modulesDirectories: ["node_modules"],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "cash",
        }),
    ],
    devServer: {
        historyApiFallback: true,
        noInfo: true
    },
    devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map'
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        })
    ])
}
