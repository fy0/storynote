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

    ga('set', 'page', location.pathname + location.hash)    
    ga('send', 'pageview');
});

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')


// markdown 渲染和代码高亮
import marked from 'marked'
import Prism from 'prismjs'
// import "prismjs/themes/prism-okaidia.css" ..备选1
import "prismjs/themes/prism-tomorrow.css" //备选2
// import './assets/css/prism-atom-dark.css'
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
import 'prismjs/components/prism-nginx.js'

let renderer = new marked.Renderer();

renderer.code = function(code, lang, escaped) {
    if (this.options.highlight) {
        var out = this.options.highlight(code, lang);
        // 这里存在问题，对部分简单代码来说 out == code 是完全可能的
        // 但是 escape 之后代价就是例如空格转换成%20，用户看来是成了乱码
        //if (out != null && out !== code) {
        if (out != null) {
            escaped = true;
            code = out;
        }
    }
  
    if (!lang) {
        return `<pre class="${this.options.langPrefix}PLACEHOLDER"><code>`
            // + (escaped ? code : escape(code, true))
            + code
            + '\n</code></pre>';
    }

    let langText = this.options.langPrefix + escape(lang, true);
    return `<pre class="${langText}"><code class="${langText}">`
        + (escaped ? code : escape(code, true))
        + '\n</code></pre>\n';
};


marked.setOptions({
    renderer: renderer,
    sanitize: true,
    langPrefix: 'language-',
    highlight: function (code, lang) {
        if (lang) {
            let stdlang = lang.toLowerCase();
            if (Prism.languages[stdlang]) {
                return Prism.highlight(code, Prism.languages[stdlang]);
            }
        }
    }
})

document.title = config.title;
