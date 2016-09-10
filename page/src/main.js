import Vue from 'vue'
import VueRouter from 'vue-router'

import "purecss"
import "./assets/css/bass.css"

import App from './app.vue'
import Index from './components/index.vue'
import TopicNew from './components/new.vue'
import ArticleList from './components/alist.vue'

Vue.use(VueRouter)

var routes = [
    { path: '/', component: Index },
    { path: '/new', component: TopicNew },
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
