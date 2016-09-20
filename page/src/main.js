import Vue from 'vue'
import VueRouter from 'vue-router'

import "purecss"
import "simplemde/dist/simplemde.min.css"
import "./assets/css/base.css"
import tools from "./tools.js"
import state from "./state.js"

import App from './app.vue'
import Index from './components/index.vue'
import TopicNew from './components/new.vue'
import TopicPage from './components/topic.vue'
import ArticleList from './components/alist.vue'
import SignIn from './components/signin.vue'
import SignUp from './components/signup.vue'

Vue.use(VueRouter)

var routes = [
    { path: '/', component: Index },
    { path: '/new', component: TopicNew},
    { path: '/t/:id(\\d+)', component: TopicPage },
    { path: '/new', component: TopicNew },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
]

var router = new VueRouter({
    routes: routes
})

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')
