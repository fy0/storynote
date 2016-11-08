
import config from "./config.js"

let API_SERVER = config.remote.API_SERVER;

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

    topicGet: async function (id) {
        try {
            let resp = await get(`${API_SERVER}/api/topic/${id}`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
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

    topicNew: async function (title, content) {
        try {
            let resp = await post(`${API_SERVER}/api/topic/new`, {title, content});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userInfo: async function () {
        try {
            let resp = await post(`${API_SERVER}/api/userinfo`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignup: async function (username, password) {
        try {
            let resp = await post(`${API_SERVER}/api/signup`, {username, password});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignin: async function (username, password) {
        try {
            let resp = await post(`${API_SERVER}/api/signin`, {username, password});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignout: async function() {
        try {
            let resp = await post(`${API_SERVER}/api/signout`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },
}
