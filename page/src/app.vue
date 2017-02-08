<template>
<div id="app">
    <div class="ic-container">
        <h1 class="page-header"><router-link :to="{ path: '/' }">SINGLE PAGE</router-link></h1>
        <div class="nav" v-if="state.data.user">
            <a href="#">标签</a>
            <a href="#">文章</a>
            <a href="#">项目</a>
            <router-link :to="{ path: '/new' }">新建</router-link>
        </div>
        <!-- 正文 -->
        <div class="pure-g">
            <div class="pure-u-6-24 left-bar">
                <ul class="nav-bar">
                    <li><a href="#">主页</a></li>
                    <li><a href="#">关于</a></li>
                </ul>
            </div>
            <div class="pure-u-18-24">
                <router-view></router-view>
            </div>
        </div>
    </div>
</div>
</template>

<style>
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
</style>

<script>
import Vue from 'vue'
import api from "./netapi.js"
import state from "./state.js"
import MsgTip from './components/msgtip.vue'

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
        'msg-tip': MsgTip
    }
}
</script>
