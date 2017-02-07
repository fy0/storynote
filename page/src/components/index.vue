<template>
<div>
    <div class="nav" v-if="state.data.user">
        <a href="#">标签</a>
        <a href="#">文章</a>
        <a href="#">项目</a>
        <router-link :to="{ path: '/new' }">新建</router-link>
    </div>
    <h1 class="page-header">SINGLE PAGE</h1>
    <div class="pure-g">
        <div class="pure-u-6-24 left-bar">
            <ul class="nav-bar">
                <li><a href="#">主页</a></li>
                <li><a href="#">关于</a></li>
            </ul>
        </div>
        <div class="pure-u-18-24">
            <div v-if="page_info.items">
                <div class="topic-item" v-for="item in page_info.items">
                    <h3 class="title">
                        <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
                    </h3>
                    <p class="info">{{time_to_text(item.time)}}</p>
                    <div class="divider-line"></div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style>

.left-bar {
}

.page-header {
    text-align: center;
}

.topic-item > .title {
    font-weight: normal;
}

.topic-item > .info {
    color: rgb(153, 153, 153);
    font-size: small;
}
</style>

<script>
import Vue from 'vue'
import api from "../netapi.js"
import state from "../state.js"

export default {
    data () {
        return {
            page_info: {},
            state: state,
        }
    },
    methods: {
        time_to_text: $.time_to_text,
    },
    mounted: async function () {
        let ret = await api.recent();
        console.log(ret)
        this.$set(this, "page_info", ret.data);

        ret = await api.userInfo();
        if (ret.code == 0) {
            Vue.set(state.data, 'user', ret.user);
        }
    }
}
</script>

<style>
    .nav {
        float: right;
    }

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

    .nav-bar a {
        color: black;
    }
    .nav-bar a:hover {
        color: black;
    }


    .nav-bar > li {
        margin-bottom: 15px;
    }

    .topic-item {
    }

    .divider-line {
        border-bottom: #EBF2F6 1px solid;
        width: 50%;
    }

    .avatar {
        float: left;
        width: 50px;
        height: 50px;
        min-height: 50px;
        border-bottom-width: 0px !important; /* fix for entry.css */
    }
</style>
