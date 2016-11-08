
let config = {
    remote: {
        API_SERVER: 'http://127.0.0.1:9000',
        REQUEST_TIMEOUT: 3000,
        ERR_TIMEOUT: -254,
        ERR_REUQEST_FAIL: -253,
    },
}


try {
    let pri = require("../private.js")
    config.remote.API_SERVER = pri.default.remote.API_SERVER || config.remote.API_SERVER;
} catch (e) {}

export default config;
