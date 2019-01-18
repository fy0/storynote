import config from './config.js'
import axios from 'axios'

axios.defaults.retry = 2
axios.defaults.retryDelay = 300

let remote = config.remote

const backend = axios.create({
    timeout: 5000,
    withCredentials: true,
    headers: {}
})

backend.interceptors.response.use(function (response) {
    // Do something with response data
    return response
}, function (error) {
    console.log(111, error)
    // Do something with response error
    // alert('请求服务器超时！将刷新页面重试！')
    setTimeout(() => {
        // window.location.reload()
    }, 3000)
    // return Promise.reject(error);
})

// function paramSerialize (obj) {
//     let str = []
//     for (let i of Object.keys(obj)) {
//         str.push(encodeURIComponent(i) + '=' + encodeURIComponent(obj[i]))
//     }
//     return str.join('&')
// }

// async function postForm (url, form) {
// let fetchParams = {
//     method: 'POST',
//     credentials: 'omit',
//     headers: {
//         'Accept': 'application/json'
//     }
// }
// fetchParams.body = form
// return (await fetch(url, fetchParams)).json()
// }

async function nget (url, params) {
    let resp = await backend.get(url, {
        params: params
    })
    if (resp) {
        if (typeof resp.data === 'string') {
            return JSON.parse(resp.data)
        }
        return resp.data
    }
}

async function npost (url, data) {
    let resp = await backend.post(url, data, {})
    if (resp) {
        if (typeof resp.data === 'string') {
            return JSON.parse(resp.data)
        }
        return resp.data
    }
}

let retcode = {
    SUCCESS: 0,
    TOO_LONG: -248,
    TOO_SHORT: -249,
    INVALID_PARAMS: -250,
    ALREADY_EXISTS: -251,
    NOT_FOUND: -252,
    UNKNOWN: -253,
    NOT_USER: -255,
    PERMISSION_DENIED: -254
}

let retinfo = {
    [retcode.SUCCESS]: '操作已成功完成',
    [retcode.TOO_LONG]: '参数过长',
    [retcode.TOO_SHORT]: '参数过短',
    [retcode.INVALID_PARAMS]: '参数缺失或值非法',
    [retcode.ALREADY_EXISTS]: '已存在',
    [retcode.NOT_FOUND]: '不存在的对象',
    [retcode.UNKNOWN]: '未知错误',
    [retcode.NOT_USER]: '未登录',
    [retcode.PERMISSION_DENIED]: '无权限'
}

export default {
    retcode,
    retinfo,

    /** 获取综合信息 */
    misc: async function (page = 1) {
        return nget(`${remote.API_SERVER}/api/misc`)
    },

    qn: async function () {
        return nget(`${remote.API_SERVER}/api/qn`)
    },

    qnUpload: async function (file) {
        let code = (await this.qn()).data
        let form = new FormData()

        form.append('token', code)
        form.append('file', file)
        form.append('accept', '')
        return npost(config.qiniu.server, form)
    },

    /** 获取文章 */
    recent: async function (page = 1) {
        return nget(`${remote.API_SERVER}/api/recent/${page}`)
    },

    /** 时间线 */
    timeline: async function (page = 1) {
        return nget(`${remote.API_SERVER}/api/timeline/${page}`)
    },

    /** 评论 - 获取 */
    commentGet: async function (topicId, page = 1) {
        return nget(`${remote.API_SERVER}/api/comment/${topicId}`, { page })
    },

    /** 评论 - 发表 */
    commentPost: async function (topicId, content) {
        return npost(`${remote.API_SERVER}/api/comment/${topicId}`, { content })
    },

    /** 评论 - 删除 */
    commentDel: async function (commentId) {
        return npost(`${remote.API_SERVER}/api/comment/del/${commentId}`)
    },

    /** 主题 - 获取内容 */
    topicGet: async function (id) {
        return nget(`${remote.API_SERVER}/api/topic/${id}`)
    },

    /** 主题 - 发表 */
    topicNew: async function (data) {
        return npost(`${remote.API_SERVER}/api/topic/new`, data)
    },

    /** 主题 - 编辑 */
    topicEdit: async function (topicId, data) {
        return npost(`${remote.API_SERVER}/api/topic/edit/${topicId}`, data)
    },

    /** 主题 - 删除 */
    topicDel: async function (topicId) {
        return npost(`${remote.API_SERVER}/api/topic/del/${topicId}`)
    },

    /** 标签 - 定义 */
    tagDefine: async function (name, desc) {
        return npost(`${remote.API_SERVER}/api/tag/define`, { name, desc })
    },

    /** 标签 - 获取 */
    tagList: async function () {
        return nget(`${remote.API_SERVER}/api/tag/list`)
    },

    /** 标签 - 获取 */
    tagGetTopics: async function (tagName) {
        return nget(`${remote.API_SERVER}/api/tag/get_topics_by_tag`, { 'tag_name': tagName })
    },

    /** 标签 - 添加至主题 */
    tagAddToTopic: async function (tagName, topicId, add_tag_if_not_exist = false) {
        return npost(`${remote.API_SERVER}/api/tag/add_to_topic`, { 'tag_name': tagName, 'topic_id': topicId, add_tag_if_not_exist })
    },

    /** 标签 - 从主题移除 */
    tagRemoveFromTopic: async function (tagName, topicId) {
        return npost(`${remote.API_SERVER}/api/tag/remove_from_topic`, { 'tag_name': tagName, 'topic_id': topicId })
    },

    /** 标签 - 根据记录ID移除标签 */
    tagRemoveFromPostById: async function (id) {
        return npost(`${remote.API_SERVER}/api/tag/remove_from_post_by_id`, { id })
    },

    /** 用户 - 注册 */
    userSignup: async function (username, password) {
        return npost(`${remote.API_SERVER}/api/user/signup`, { username, password })
    },

    /** 用户 - 登陆 */
    userSignin: async function (username, password, remember) {
        return npost(`${remote.API_SERVER}/api/user/signin`, { username, password, remember })
    },

    /** 用户 - 注销 */
    userSignout: async function () {
        return npost(`${remote.API_SERVER}/api/user/signout`)
    },

    /** 用户 - 个人信息 */
    userInfo: async function () {
        return nget(`${remote.API_SERVER}/api/user/userinfo`)
    },

    userInfo2: async function (headers) {
        let resp = await backend.get(`${remote.API_SERVER}/api/user/userinfo`, {
            headers
        })
        if (resp) {
            if (typeof resp.data === 'string') {
                return JSON.parse(resp.data)
            }
            return resp.data
        }
    },

    /** 用户 - 修改密码 */
    userPWChange: async function (password, newPassword) {
        return npost(`${remote.API_SERVER}/api/user/password_change`, { password, 'new_password': newPassword })
    },

    /** 管理 - 用户 - 列表 */
    manageUserList: async function (keyword = '', p = 1) {
        return nget(`${remote.API_SERVER}/api/manage/user`, { keyword, p })
    },

    /** 管理 - 用户 - 重置密码 */
    manageUserPasswordReset: async function (userId, newPassword) {
        return npost(`${remote.API_SERVER}/api/manage/user/password_reset`, { 'user_id': userId, 'new_password': newPassword })
    },

    /** 管理 - 用户 - 重置key */
    manageUserKeyReset: async function (userId) {
        return npost(`${remote.API_SERVER}/api/manage/user/key_reset`, { 'user_id': userId })
    },

    /** 管理 - 用户 - 修改用户组 */
    manageUserChangeLevel: async function (userId, level) {
        return npost(`${remote.API_SERVER}/api/manage/user/change_level`, { 'user_id': userId, level })
    },

    /** 管理 - 主题 - 列表 */
    manageTopicList: async function (p = 1) {
        return nget(`${remote.API_SERVER}/api/manage/topic`, { p })
    },

    /** 管理 - 主题 - 修改状态 */
    manageUserChangeState: async function (topicId, state) {
        return npost(`${remote.API_SERVER}/api/manage/topic/change_state`, { 'topic_id': topicId, state })
    }
}
