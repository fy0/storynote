
let config = {
    remote: {
        // API_SERVER: 'http://api.fy0.me',
        API_SERVER: 'http://localhost:9000',
        REQUEST_TIMEOUT: 3000,
        ERR_TIMEOUT: -254,
        ERR_REUQEST_FAIL: -253,
    },
    title: '世界边缘，fy 的摸鱼之地',
}


try {
    let pri = require("../private.js")
    config.remote.API_SERVER = pri.default.remote.API_SERVER || config.remote.API_SERVER;
} catch (e) {}

export default config;
