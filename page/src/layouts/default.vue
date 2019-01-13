<template>
<div id="app">
    <div class="ic-container">
        <!-- header -->
        <div class="page-header">
            <h1><nuxt-link style="outline: none;" :to="{ path: '/' }">{{config.title.toUpperCase()}}</nuxt-link></h1>
        </div>
        <!-- 正文 -->
        <div class="main-box">
            <div class="left">
                <ul class="nav-bar">
                    <nuxt-link tag="li" :to="{ name: 'index' }" :class="navActiveClass('index', 'topic')"><a>日志</a></nuxt-link>
                    <nuxt-link tag="li" :to="{ name: 'tags' }" :class="navActiveClass('tag', 'tags')"><a>标签</a></nuxt-link>
                    <nuxt-link tag="li" :to="{ name: 'timeline' }" :class="navActiveClass('timeline')"><a>时光</a></nuxt-link>
                    <nuxt-link tag="li" :to="{ path: '/signin' }" :class="navActiveClass('signin', 'signup', 'signout')"><a>用户</a></nuxt-link>
                    <no-ssr placeholder="">
                        <template>
                            <nuxt-link v-if="user && user.level >= 80" tag="li" :to="{ path: '/new' }" :class="navActiveClass('topic_new', 'topic_edit')"><a>新建</a></nuxt-link>
                            <nuxt-link v-if="user && user.level >= 100" tag="li" :to="{ path: '/manage' }" :class="navActiveClass('manage')"><a>管理</a></nuxt-link>
                        </template>
                    </no-ssr>
                    <nuxt-link tag="li" :to="{ name: 'links' }" :class="navActiveClass('links')"><a>友链</a></nuxt-link>
                    <nuxt-link tag="li" :to="{ path: '/about' }" :class="navActiveClass('about')"><a>关于</a></nuxt-link>
                </ul>
            </div>
            <div class="content">
                <nuxt />
            </div>
        </div>
        <!-- footer -->
        <footer><p>Copyright © 2017 <a target="_blank" href="http://github.com/fy0/storynote">Story Note</a></p></footer>
        <no-ssr>
            <msg-box></msg-box>
            <go-top></go-top>
        </no-ssr>
    </div>
</div>
</template>

<style lang="scss">
@import '../assets/css/base.css';

.main-box {
    min-height: 40vh;
    display: flex;

    > .left {
        flex: 6 0 0%;
        width: 0%;
    }

    > .content {
        flex: 18 0 0%;
        width: 0%;
        word-break: break-all;
    }
}
</style>

<style>
footer {
    text-align: center;
    margin-top: 40px;
    color: #aaa;
}
/*.main-box { min-height: 70vh; }*/
.nav-top { margin-top: -30px; }
.nav-bar {
    height: 100%;
    font-size: 1.10em;
    padding-top: 3px;
    padding-right: 20px;
    margin-right: 20px;
    text-align: right;
    list-style-type: none;
    border-right: 1px solid #ccc;
    font-weight: bolder;
}
.nav-bar a { color: black; }
.nav-bar a:hover { color: black; }
.nav-bar li { margin-bottom: 15px; }
.page-header { text-align: center; }
.page-header > h2 { margin: 0; }

.nav-bar > li.link-active > a {
    text-decoration-line: underline;
    text-underline-position: under;
}

.nav-bar > li.nuxt-link-active:not(.flag) > a {
    text-decoration-line: underline;
    text-underline-position: under;
}
</style>

<script>
import config from '@/config.js'
import state from '@/state.js'
// import Loading from './components/utils/loading.vue'
import MsgBox from '@/components/utils/msgbox.vue'
import GoTop from '@/components/utils/gotop.vue'
// import ErrorPage from './components/ErrorPage.vue'

export default {
    data () {
        return {
            state,
            config
        }
    },

    computed: {
        user: function () {
            return this.state.data.user || {}
        },
        error () {
            return this.$store.state.errorHandler.error
        }
    },

    head () {
        return {
            title: '',
            titleTemplate: function (val) {
                if (val) {
                    return `${val} - ${config.title}`
                }
                return config.title
            },
            htmlAttrs: {
                lang: 'zh'
            },
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { hid: 'description', name: 'description', content: '我的个人博客' }
            ],
            link: [
                { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
            ]
        }
    },

    components: {
        GoTop,
        MsgBox
    },

    methods: {
        navActiveClass: function (...names) {
            for (let name of names) {
                if (name === this.$route.name) {
                    return 'link-active'
                }
            }
            return 'flag'
        }
    }
}
</script>
