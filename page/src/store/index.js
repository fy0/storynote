// import Vue from 'vue'
// import api from '@/netapi'
// import myState from '@/state'

export const state = () => ({
    counter: 0
})

export const mutations = {
    increment (state) {
        state.counter++
    }
}

export const actions = {
    async nuxtServerInit ({ commit }, { req }) {
        // if (!myState.data.misc) {
        // let ret = await api.misc()
        // Vue.set(myState.data, 'misc', ret.data)
        // commit('SET_MISC', ret.data)
        // }
    }
}
