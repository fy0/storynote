import Vue from 'vue'
import VueRouter from 'vue-router'

import 'lodash'
import 'purecss'
import 'animate.css'
import 'font-awesome/css/font-awesome.css'
import 'simplemde/dist/simplemde.min.css'
import './assets/css/base.css'
import tools from './tools.js'
import state from './state.js'
import api from "./netapi.js"

import App from './app.vue'
import Index from './components/index.vue'
import Timeline from './components/timeline.vue'
import TopicPage from './components/topic.vue'
import TopicNew from './components/topic_new.vue'
import Tags from './components/tags.vue'
import TagPage from './components/tag.vue'
import SignIn from './components/user/signin.vue'
import SignUp from './components/user/signup.vue'
import SignOut from './components/user/signout.vue'
import Loading from './components/utils/loading.vue'
import Manage from './components/manage.vue'
import About from './components/about.vue'

import { Button, Card, Checkbox, DatePicker, Dialog, Select, TabPane, Tabs, Tag, Input, Form, FormItem, MessageBox } from 'element-ui'
Vue.use(Button)
Vue.use(Card)
Vue.use(Checkbox)
Vue.use(DatePicker)
Vue.use(Dialog)
Vue.use(Select)
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

Vue.component('my-title', {
    props: ['size', 'text', 'aaa'],
    render: function (createElement) {
        document.title = this.text;
    },
    mounted: function () {
    }
})

Vue.use(VueRouter)

var routes = [
    // 注意：router的exact针对的是path而不是对象本身，因此虽然模板中指定的
    // 是 name: index 但意味着“主页”链接永远带有 router-link-active
    // { path: '/', component: Index },
    // { path: '/p/:page(\\d+)?', name: 'index', component: Index },
    { path: '/:p(p)?/:page(\\d+)?', name: 'index', component: Index },
    { path: '/timeline/:page(\\d+)?', name: 'timeline', component: Timeline },
    { path: '/new', component: TopicNew},
    { path: '/t/:id(\\d+)/:cmtpage(\\d+)?', name: 'topic', component: TopicPage },
    { path: '/tags', name: 'tags', component: Tags },
    { path: '/tag/:name(\\S+)', name: 'tag', component: TagPage },
    { path: '/new', component: TopicNew },
    { path: '/edit/t/:id(\\d+)', component: TopicNew },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
    { path: '/signout', component: SignOut },
    { path: '/manage', name: 'manage', component: Manage },
    { path: '/about', component: About },
    { path: '/loading', component: Loading },
]

var router = new VueRouter({
    mode: 'hash',
    routes: routes
})

router.beforeEach(async function (to, from, next)  {
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

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')


// markdown 渲染和代码高亮
import marked from 'marked'
import Prism from 'prismjs'
import "prismjs/themes/prism.css"
// prism 默认包含高亮：
// ["extend", "insertBefore", "DFS", "markup", "xml", "html", "mathml", "svg", "css", "clike", "javascript", "js"]
import 'prismjs/components/prism-autohotkey.js'
import 'prismjs/components/prism-bash.js'
import 'prismjs/components/prism-batch.js'
import 'prismjs/components/prism-c.js'
import 'prismjs/components/prism-clike.js'
import 'prismjs/components/prism-cpp.js'
import 'prismjs/components/prism-csharp.js'
import 'prismjs/components/prism-css.js'
import 'prismjs/components/prism-css-extras.js'
import 'prismjs/components/prism-git.js'
import 'prismjs/components/prism-glsl.js'
import 'prismjs/components/prism-go.js'
import 'prismjs/components/prism-ini.js'
import 'prismjs/components/prism-java.js'
import 'prismjs/components/prism-javascript.js'
import 'prismjs/components/prism-json.js'
import 'prismjs/components/prism-lua.js'
import 'prismjs/components/prism-markdown.js'
import 'prismjs/components/prism-python.js'
import 'prismjs/components/prism-sql.js'


marked.setOptions({
    renderer: new marked.Renderer(),
    sanitize: true,
    highlight: function (code, lang) {
        if (lang) {
            let stdlang = lang.toLowerCase();
            if (Prism.languages[stdlang]) {
                return Prism.highlight(code, Prism.languages[stdlang]);
            }
        }
    }
})
