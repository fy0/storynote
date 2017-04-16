<template>
<div id="app">
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
                    <li><router-link :to="{ path: '/signin' }">用户</router-link></li>
                    <li v-if="state.data.user"><router-link :to="{ path: '/new' }">撰文</router-link></li>
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
    padding-top: 10px;
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
import Loading from "./components/loading.vue"
import MsgBox from './components/msgbox.vue'
import GoTop from './components/gotop.vue'

export default {
    data () {
        return {
            state: state,
        }
    },
    mounted: async function () {
        let ret = await api.misc();
        Vue.set(state.data, 'misc', ret.data);

        ret = await api.userInfo();
        //console.log(ret);
        if (ret.code == 0) {
            Vue.set(state.data, 'user', ret.data);
        }
    },
    components: {
        // <my-component> 将只在父模板可用
        GoTop,
        'msg-box': MsgBox
    }
}
</script>
