import Vue from 'vue'
import App from './App.vue'
import createRouter from './router'
import createStore from './store'

// import nprogress from 'nprogress/nprogress.js'
import 'purecss'

import 'lodash'
import 'animate.css'
// import 'nprogress/nprogress.css'

import './assets/css/base.css'
import state from './state.js'
import api from './netapi.js'
import './tools.js'
import './config.js'

// import { Button, Card, Checkbox, DatePicker, Dialog, Select, Option, TabPane, Tabs, Tag, Input, Form, FormItem, MessageBox } from 'element-ui'

Vue.config.productionTip = false

// Vue.use(Button)
// Vue.use(Card)
// Vue.use(Checkbox)
// Vue.use(DatePicker)
// Vue.use(Dialog)
// Vue.use(Select)
// Vue.use(Option)
// Vue.use(TabPane)
// Vue.use(Tabs)
// Vue.use(Tag)
// Vue.use(Input)
// Vue.use(Form)
// Vue.use(FormItem)

// MessageBox 处理
// Vue.prototype.$msgbox = MessageBox
// Vue.prototype.$alert = MessageBox.alert
// Vue.prototype.$confirm = MessageBox.confirm
// Vue.prototype.$prompt = MessageBox.prompt

// document.title = config.title

export default () => {
    const store = createStore()
    const router = createRouter()

    router.beforeEach(async function (to, from, next) {
        // nprogress.start()

        next()
    })

    router.afterEach(async function (to, from, next) {
        // nprogress.done()
        // setInterval(() => {
        //     ga('set', 'page', location.pathname + location.hash)
        //     ga('send', 'pageview');
        // }, 0)
    })

    return new Vue({
        router,
        store,
        render: h => h(App)
    })
}
