<template>
<div id="app">
    <my-title :text='config.title'></my-title>
    <div class="ic-container">
        <!-- header -->
        <div class="page-header">
            <h1><router-link :to="{ path: '/' }">{{config.title.toUpperCase()}}</router-link></h1>
        </div>
        <!-- 正文 -->
        <div class="pure-g main-box">
            <div class="pure-u-6-24 left-bar">
                <ul class="nav-bar">
                    <router-link tag="li" :to="{ name: 'index' }" :class="is_index"><a>故事</a></router-link>
                    <router-link tag="li" :to="{ name: 'timeline' }" ><a>时光</a></router-link>
                    <router-link tag="li" :to="{ path: '/signin' }" ><a>用户</a></router-link>
                    <router-link v-if="state.data.user" tag="li" :to="{ path: '/new' }" ><a>撰文</a></router-link>
                    <router-link v-if="state.data.user" tag="li" :to="{ path: '/manage' }" ><a>管理</a></router-link>
                    <router-link tag="li" :to="{ path: '/about' }" ><a>关于</a></router-link>
                </ul>
            </div>
            <div class="pure-u-18-24">
                <router-view></router-view>
            </div>
        </div>
        <!-- footer -->
        <footer><p>Copyright © 2017 <a href="">{{config.powered_by}}</a></p></footer>
    </div>
    <msg-box></msg-box>
    <go-top></go-top>
</div>
</template>

<style>
footer {
    text-align: center;
    margin-top: 40px;
    color: #aaa;
}
/*.main-box { min-height: 70vh; }*/
.main-box { min-height: 40vh; }
.nav-top { margin-top: -30px; }
.nav-bar {
    height: 100%;
    font-size: 1.1em;
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
.nav-bar > li { margin-bottom: 15px; }
.page-header { text-align: center; }
.page-header > h2 { margin: 0; }

.nav-bar > li.router-link-active:not(.index-flag) > a {
    text-decoration-line: underline;
    text-underline-position: under;
}

.nav-bar > li.nav-active > a {

}
</style>

<script>
import Vue from 'vue'
import api from "./netapi.js"
import state from "./state.js"
import config from "./config.js"
import Loading from "./components/utils/loading.vue"
import MsgBox from './components/utils/msgbox.vue'
import GoTop from './components/utils/gotop.vue'

export default {
    data () {
        return {
            state,
            config,
        }
    },
    computed: {
        is_index: function () {
            if (this.$route.name != 'index') {
                return 'index-flag';
            }
            if (this.$route.name == 'topic') {
                return 'nav-active';
            }
        }
    },
    mounted: async function () {
    },
    components: {
        // <my-component> 将只在父模板可用
        GoTop,
        'msg-box': MsgBox
    }
}
</script>
