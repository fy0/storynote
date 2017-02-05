
import config from "./config.js"

let remote = config.remote;

function paramSerialize (obj) {
    let str = [];
    for (let i of Object.keys(data)) {
        str.push(encodeURIComponent(i) + "=" + encodeURIComponent(obj[i]));
    }
    return str.join("&");
}

async function do_fetch(url, method, data, fix) {
    let fetchParams = {
        method: method,
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }
    if (method == 'GET') if (data) url += `?${paramSerialize(data)}`;
    if (method == 'POST') fetchParams.body = JSON.stringify(data);
    return fetch(url, fetchParams);
}

async function get (url, data, fix) { return do_fetch(url, "GET", data, fix); }
async function post (url, data, fix) { return do_fetch(url, "POST", data, fix); }

async function nget(url, info) {
    try {
        let resp = await get(url, info);
        if (!resp.ok) throw "NOT 200";
        let data = await resp.json();
        return data;
    } catch(e) {
        console.log("Oops, error", e);
    }
}

async function npost(url, info) {
    try {
        let resp = await post(url, info);
        if (!resp.ok) throw "NOT 200";
        let data = await resp.json();
        return data;
    } catch(e) {
        console.log("Oops, error", e);
    }
}

export default {
    /** 获取文章 */
    recent: async function (page=1) {
        return await nget(`${remote.API_SERVER}/api/recent/${page}`);
    },

    /** 评论 - 获取 */
    replyGet: async function (topic_id) {
        return await nget(`${remote.API_SERVER}/api/reply/${topic_id}`);
    },

    /** 评论 - 发表 */
    replyPost: async function (topic_id) {
        return await npost(`${remote.API_SERVER}/api/reply/${topic_id}`);
    },

    /** 评论 - 删除 */
    replyDel: async function (reply_id) {
        return await npost(`${remote.API_SERVER}/api/reply/del/${reply_id}`);
    },

    /** 主题 - 获取内容 */
    topicGet: async function (id) {
        return await nget(`${remote.API_SERVER}/api/topic/${id}`);
    },

    /** 主题 - 发表 */
    topicNew: async function (title, content) {
        return await npost(`${remote.API_SERVER}/api/topic/new`, {title, content});
    },

    /** 主题 - 编辑 */
    topicEdit: async function (topic_id, title, content) {
        return await npost(`${remote.API_SERVER}/api/topic/edit/${topic_id}`, {title, content});
    },

    /** 主题 - 删除 */
    topicDel: async function (topic_id) {
        return await npost(`${remote.API_SERVER}/api/topic/del/${topic_id}`);
    },

    /** 用户 - 注册 */
    userSignup: async function (username, password) {
        return await npost(`${remote.API_SERVER}/api/user/signup`, {username, password});
    },

    /** 用户 - 登陆 */
    userSignin: async function (username, password) {
        return await npost(`${remote.API_SERVER}/api/user/signin`, {username, password});
    },

    /** 用户 - 注销 */
    userSignout: async function () {
        return await npost(`${remote.API_SERVER}/api/user/signout`);
    },

    /** 用户 - 个人信息 */
    userInfo: async function () {
        return await npost(`${remote.API_SERVER}/api/user/userinfo`);
    },

    /** 用户 - 修改密码 */
    userPWChange: async function (password, new_password) {
        return await npost(`${remote.API_SERVER}/api/user/password_change`, {password, new_password});
    },
}
