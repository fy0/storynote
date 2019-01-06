import Vue from 'vue'
import Vuex from 'vuex'
import api from './netapi'
import state from './state'

Vue.use(Vuex)

export default () => {
    return new Vuex.Store({
        state: {
            misc: null,
            user: null
        },
        mutations: {
            // 设置
            SET_MISC (state, data) {
                state.misc = data
            },
            SET_USER (state, data) {
                state.user = data
            }
        },
        actions: {
            async onHttpRequest ({ store, commit }) {
                if (!state.data.misc) {
                    let ret = await api.misc()
                    Vue.set(state.data, 'misc', ret.data)
                    commit('SET_MISC', ret.data)

                    ret = await api.userInfo()
                    console.log('user', ret)
                    if (ret.code === 0) {
                        commit('SET_USER', ret.data)
                        Vue.set(state.data, 'user', ret.data)
                    }
                }
            }
        }
    })
}
