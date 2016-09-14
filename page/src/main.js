import Vue from 'vue'
import VueRouter from 'vue-router'

import "purecss"
import "simplemde/dist/simplemde.min.css"
import "./assets/css/bass.css"
import "./tools.js"

import App from './app.vue'
import Index from './components/index.vue'
import TopicNew from './components/new.vue'
import TopicPage from './components/topic.vue'
import ArticleList from './components/alist.vue'

Vue.use(VueRouter)

var routes = [
    { path: '/', component: Index },
    { path: '/new', component: TopicNew },
    { path: '/t/:id(\\d+)', component: TopicPage },
    { path: '/foo', component: ArticleList },
]

var router = new VueRouter({
    routes: routes
})

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')
