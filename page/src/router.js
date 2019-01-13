import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/index.vue'
import Timeline from '@/components/timeline.vue'
import TopicPage from '@/components/topic.vue'
import Tags from '@/components/tags.vue'
import TagPage from '@/components/tag.vue'
import SignIn from '@/components/user/signin.vue'
import SignUp from '@/components/user/signup.vue'
import SignOut from '@/components/user/signout.vue'
import Loading from '@/components/utils/loading.vue'
import Manage from '@/components/manage.vue'
import Links from '@/components/links.vue'
import About from '@/components/about.vue'

const TopicNew = () => import('@/components/topic_new.vue')

Vue.use(Router)

export function createRouter () {
    let router = new Router({
        mode: 'history',
        base: process.env.BASE_URL,
        routes: [
            // {
            //     path: '/',
            //     name: 'home',
            //     component: Home
            // },
            // 注意：router的exact针对的是path而不是对象本身，因此虽然模板中指定的
            // 是 name: index 但意味着“主页”链接永远带有 nuxt-link-active
            { path: '/', component: Index },
            // { path: '/p/:page(\\d+)?', name: 'index', component: Index },
            { path: '/:p(p)?/:page(\\d+)?', name: 'index', component: Index },
            { path: '/timeline/:page(\\d+)?', name: 'timeline', component: Timeline },
            { path: '/new', name: 'topic_new', component: TopicNew },
            { path: '/t/:id(\\d+)/:cmtpage(\\d+)?', name: 'topic', component: TopicPage },
            { path: '/tags', name: 'tags', component: Tags },
            { path: '/tag/:name(\\S+)', name: 'tag', component: TagPage },
            { path: '/edit/t/:id(\\d+)', name: 'topic_edit', component: TopicNew },
            { path: '/signin', component: SignIn },
            { path: '/signup', component: SignUp },
            { path: '/signout', component: SignOut },
            { path: '/manage', name: 'manage', component: Manage },
            { path: '/links', name: 'links', component: Links },
            { path: '/about', component: About },
            { path: '/loading', component: Loading }
        ]
    })

    return router
}
