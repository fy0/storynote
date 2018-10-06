import Vue from 'vue'
import VueRouter from 'vue-router'
import nprogress from 'nprogress/nprogress.js'

import 'lodash'
import 'purecss'
import 'animate.css'
import 'nprogress/nprogress.css'
import 'font-awesome/css/font-awesome.css'

import './assets/css/base.css'
import tools from './tools.js'
import state from './state.js'
import api from "./netapi.js"
import config from './config.js'

import App from './app.vue'
import Index from './components/index.vue'
import Timeline from './components/timeline.vue'
import TopicPage from './components/topic.vue'
const TopicNew = () => import('./components/topic_new.vue')
import Tags from './components/tags.vue'
import TagPage from './components/tag.vue'
import SignIn from './components/user/signin.vue'
import SignUp from './components/user/signup.vue'
import SignOut from './components/user/signout.vue'
import Loading from './components/utils/loading.vue'
import Manage from './components/manage.vue'
import Links from './components/links.vue'
import About from './components/about.vue'

import { Button, Card, Checkbox, DatePicker, Dialog, Select, Option, TabPane, Tabs, Tag, Input, Form, FormItem, MessageBox } from 'element-ui'
Vue.use(Button)
Vue.use(Card)
Vue.use(Checkbox)
Vue.use(DatePicker)
Vue.use(Dialog)
Vue.use(Select)
Vue.use(Option)
Vue.use(TabPane)
Vue.use(Tabs)
Vue.use(Tag)
Vue.use(Input)
Vue.use(Form)
Vue.use(FormItem)

// MessageBox 处理
Vue.prototype.$msgbox = MessageBox;
Vue.prototype.$alert = MessageBox.alert;
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$prompt  = MessageBox.prompt;

Vue.use(VueRouter)

var routes = [
    // 注意：router的exact针对的是path而不是对象本身，因此虽然模板中指定的
    // 是 name: index 但意味着“主页”链接永远带有 router-link-active
    // { path: '/', component: Index },
    // { path: '/p/:page(\\d+)?', name: 'index', component: Index },
    { path: '/:p(p)?/:page(\\d+)?', name: 'index', component: Index },
    { path: '/timeline/:page(\\d+)?', name: 'timeline', component: Timeline },
    { path: '/new', name: 'topic_new', component: TopicNew},
    { path: '/t/:id(\\d+)/:cmtpage(\\d+)?', name: 'topic', component: TopicPage },
    { path: '/tags', name: 'tags', component: Tags },
    { path: '/tag/:name(\\S+)', name: 'tag', component: TagPage },
    { path: '/edit/t/:id(\\d+)', name: "topic_edit", component: TopicNew },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
    { path: '/signout', component: SignOut },
    { path: '/manage', name: 'manage', component: Manage },
    { path: '/links', name: 'links', component: Links },
    { path: '/about', component: About },
    { path: '/loading', component: Loading },
]

var router = new VueRouter({
    //mode: 'hash',
    mode: 'history',
    routes: routes
})

router.beforeEach(async function (to, from, next)  {
    nprogress.start();

    if (!state.data.misc) {
        let ret = await api.misc();
        Vue.set(state.data, 'misc', ret.data);

        ret = await api.userInfo();
        if (ret.code == 0) {
            Vue.set(state.data, 'user', ret.data);
        }
    }

    next();
});

router.afterEach(async function (to, from, next) {
    // 我日，当组件被复用时，居然会调用 beforeEach 而不会调用 afterEach
    // 也不知道几个意思
    // reuse 坑人不浅，貌似还禁用不掉……
    nprogress.done();

    setInterval(() => {
        ga('set', 'page', location.pathname + location.hash)
        ga('send', 'pageview');
    }, 0)
});

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')

document.title = config.title
