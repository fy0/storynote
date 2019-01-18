import api from '@/netapi'
// const cookieparser = process.server ? require('cookieparser') : undefined

export const state = () => ({
    msgs: [],
    misc: null,
    user: null

    /* 实际内容动态获取
    misc: {
        USER_LEVEL: {
            'DEL': 0,
            'NORMAL': 50,
        },
        USER_LEVEL_TXT: {
            0: '删除',
            50: '正常'
        },
        TOPIC_STATE: { ... },
        TOPIC_STATE_TXT: { ... }
    }, */
})

export const mutations = {
    SET_MISC (state, val) {
        state.misc = val
    },
    SET_USERDATA (state, val) {
        state.user = val
    }
}

export const actions = {
    async init ({ state, commit }) {
    },
    async nuxtServerInit ({ commit }, { req }) {
        let ret = await api.userInfo2(req.headers)
        if (ret.code === 0) {
            commit('SET_USERDATA', ret.data)
        }
    }
}
