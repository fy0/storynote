<template>
<div id="app">
    <my-title :text='config.title'></my-title>
    <div class="ic-container">
        <!-- header -->
        <div class="page-header">
            <h1><router-link :to="{ path: '/' }">SINGLE NOTE</router-link></h1>
        </div>
        <!-- 正文 -->
        <div class="pure-g main-box">
            <div class="pure-u-6-24 left-bar">
                <ul class="nav-bar">
                    <li><router-link :to="{ path: '/' }">主页</router-link></li>
                    <li><router-link :to="{ path: '/timeline' }">时光</router-link></li>
                    <li><router-link :to="{ path: '/signin' }">用户</router-link></li>
                    <li v-if="state.data.user"><router-link :to="{ path: '/new' }">撰文</router-link></li>
                    <li v-if="state.data.user"><router-link :to="{ name: 'manage' }">管理</router-link></li>
                    <li><router-link :to="{ path: '/about' }">关于</router-link></li>
                </ul>
            </div>
            <div class="pure-u-18-24">
                <router-view></router-view>
            </div>
        </div>
        <!-- footer -->
        <footer><p>Copyright © 2017 <a href="">Single Note</a></p></footer>
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
    mounted: async function () {
    },
    components: {
        // <my-component> 将只在父模板可用
        GoTop,
        'msg-box': MsgBox
    }
}
</script>
