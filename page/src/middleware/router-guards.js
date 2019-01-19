import api from '@/netapi'

export default async function ({ store, route, redirect, req }) {
    if (!store.state.misc) {
        let ret = await api.misc()
        store.commit('SET_MISC', ret.data)

        if (process.browser) {
            ret = await api.userInfo()
            if (ret.code === 0) {
                store.commit('SET_USERDATA', ret.data)
            }
        }
    }
}
