import Vue from 'vue'
import api from '@/netapi'
import state from '@/state'

export default ({ app }) => {
    app.router.beforeEach(async function (to, from, next) {
        // nprogress.start()
        // await app.store.dispatch('init')
        let ret = await api.misc()
        Vue.set(state.data, 'misc', ret.data)

        if (process.client) {
            ret = await api.userInfo()
            if (ret.code === 0) {
                Vue.set(state.data, 'user', ret.data)
            }
        }

        next()
    })
}
