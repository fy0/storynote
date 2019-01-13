// import Vue from 'vue'
// import api from '@/netapi'
// import myState from '@/state'

export const state = () => ({
    counter: 0,
    misc: null
})

export const mutations = {
    increment (state) {
        state.counter++
    },
    SET_MISC (state, data) {
        state.misc = data
    },
    SET_USER (state, data) {
        state.user = data
    }
}

export const actions = {
    async init ({ state, commit }) {
        // if (!state.misc) {
        //     let ret = await api.misc()
        //     commit('SET_MISC', ret.data)

        //     ret = await api.userInfo()
        //     if (ret.code === 0) {
        //         commit('SET_USER', ret.data)
        //     }
        // }
    }
}
