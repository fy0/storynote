
let API_SERVER = 'http://127.0.0.1:9000'
let REQUEST_TIMEOUT = 3000

let ERR_TIMEOUT = -255
let ERR_REUQEST_FAIL = -254

let info_post = {credentials: 'include', 'method': 'POST'};
let info_get = {credentials: 'include', 'method': 'GET'};

async function do_fetch (url, method, data, fix) {
    return fetch(url, {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        credentials: 'include'
    })
}

async function get (url, data, fix) { return do_fetch(url, "GET", data, fix); }
async function post (url, data, fix) { return do_fetch(url, "POST", data, fix); }


export default {
    test: async function (username, password) {
        try {
            let resp = await post(`${API_SERVER}`, {username: '123'});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            console.log(data);
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    topicRecent: async function () {
        try {
            let resp = await get(`${API_SERVER}/api/recent`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignin: async function (username, password) {
        try {
            let resp = await post(`${API_SERVER}`, {username: '123'});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            console.log(data);
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignout: async function() {
        try {
            let resp = await post(`${API_SERVER}/api/signout`, {username: '123'});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            console.log(data);
        } catch(e) {
            console.log("Oops, error", e);
        }
    },
}
