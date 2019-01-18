import api from '@/netapi'

export default async function ({ store, route, redirect, req }) {
    let ret = await api.misc()
    store.commit('SET_MISC', ret.data)

    if (process.client) {
        ret = await api.userInfo()
        if (ret.code === 0) {
            store.commit('SET_USERDATA', ret.data)
        }
    }
}
