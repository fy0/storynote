
import 'whatwg-fetch'
import config from "./config.js"

let remote = config.remote;

function paramSerialize (obj) {
    let str = [];
    for (let i of Object.keys(obj)) {
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

let retcode = {
    SUCCESS: 0,
    ALREADY_EXISTS: -251,
    NOT_FOUND: -252,
    UNKNOWN: -253,
    NOT_USER: -255,
    PERMISSION_DENIED: -254
}

let retinfo = {
    //retcode.SUCCESS: '成功',
}

export default {
    retcode,
    retinfo,

    /** 获取综合信息 */
    misc: async function (page=1) {
        return await nget(`${remote.API_SERVER}/api/misc`);
    },

    /** 获取文章 */
    recent: async function (page=1) {
        return await nget(`${remote.API_SERVER}/api/recent/${page}`);
    },

    /** 时间线 */
    timeline: async function (page=1) {
        return await nget(`${remote.API_SERVER}/api/timeline/${page}`);
    },

    /** 评论 - 获取 */
    commentGet: async function (topic_id, page=1) {
        return await nget(`${remote.API_SERVER}/api/comment/${topic_id}`, {page});
    },

    /** 评论 - 发表 */
    commentPost: async function (topic_id, content) {
        return await npost(`${remote.API_SERVER}/api/comment/${topic_id}`, {content});
    },

    /** 评论 - 删除 */
    commentDel: async function (comment_id) {
        return await npost(`${remote.API_SERVER}/api/comment/del/${comment_id}`);
    },

    /** 主题 - 获取内容 */
    topicGet: async function (id) {
        return await nget(`${remote.API_SERVER}/api/topic/${id}`);
    },

    /** 主题 - 发表 */
    topicNew: async function (title, content, time) {
        return await npost(`${remote.API_SERVER}/api/topic/new`, {title, content, time});
    },

    /** 主题 - 编辑 */
    topicEdit: async function (topic_id, title, content) {
        return await npost(`${remote.API_SERVER}/api/topic/edit/${topic_id}`, {title, content});
    },

    /** 主题 - 删除 */
    topicDel: async function (topic_id) {
        return await npost(`${remote.API_SERVER}/api/topic/del/${topic_id}`);
    },

    /** 标签 - 定义 */
    tagDefine: async function (name, desc) {
        return await npost(`${remote.API_SERVER}/api/tag/define`, {name, desc});
    },

    /** 标签 - 获取 */
    tagList: async function () {
        return await nget(`${remote.API_SERVER}/api/tag/list`);
    },

    /** 标签 - 添加至主题 */
    tagAddToTopic: async function (tag_name, topic_id, add_tag_if_not_exist=false) {
        return await npost(`${remote.API_SERVER}/api/tag/add_to_topic`, {tag_name, topic_id, add_tag_if_not_exist});
    },

    /** 标签 - 从主题移除 */
    tagRemoveFromTopic: async function (tag_name, topic_id) {
        return await npost(`${remote.API_SERVER}/api/tag/remove_from_topic`, {tag_name, topic_id});
    },

    /** 标签 - 根据记录ID移除标签 */
    tagRemoveFromPostById: async function (id) {
        return await npost(`${remote.API_SERVER}/api/tag/remove_from_post_by_id`, {id});
    },

    /** 用户 - 注册 */
    userSignup: async function (username, password) {
        return await npost(`${remote.API_SERVER}/api/user/signup`, {username, password});
    },

    /** 用户 - 登陆 */
    userSignin: async function (username, password, remember) {
        return await npost(`${remote.API_SERVER}/api/user/signin`, {username, password, remember});
    },

    /** 用户 - 注销 */
    userSignout: async function () {
        return await npost(`${remote.API_SERVER}/api/user/signout`);
    },

    /** 用户 - 个人信息 */
    userInfo: async function () {
        return await nget(`${remote.API_SERVER}/api/user/userinfo`);
    },

    /** 用户 - 修改密码 */
    userPWChange: async function (password, new_password) {
        return await npost(`${remote.API_SERVER}/api/user/password_change`, {password, new_password});
    },
}
