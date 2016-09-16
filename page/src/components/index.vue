<template>
<div>
    <div class="nav">
        <a href="#">标签</a>
        <a href="#">文章</a>
        <a href="#">项目</a>
        <router-link :to="{ path: '/signup' }">注册</router-link>
        <router-link :to="{ path: '/signin' }">登录</router-link>
        <router-link :to="{ path: '/new' }">新建</router-link>
    </div>
    <h1>这里是标题</h1>
    <div class="pure-g">
        <div class="pure-u-3-4">
            <div v-if="page_info.items">
                <div class="topic-item" v-for="item in page_info.items">
                    <p>
                        <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
                    </p>
                    <p>{{time_to_text(item.time)}}</p>
                    <div class="divider-line"></div>
                </div>
            </div>
        </div>
        <div class="pure-u-1-4">
            <img class="avatar" src="../assets/images/doge.png"/>
        </div>
    </div>
</div>
</template>

<script>

import api from "../netapi.js"

export default {
    data () {
        return {
            page_info: {},
            msg: 'Hello Vue 2.0!'
        }
    },
    methods: {
        time_to_text: $.time_to_text,
    },
    mounted: async function () {
        let ret = await api.topicRecent();
        console.log(1111111, ret);
        this.$set(this, "page_info", ret.data);
        //ret = await api.topicNew('这是一篇文章1', "内容内容内容内容内容内容内容内容");
        //console.log(1111111, ret);
    }
}
</script>

<style>
    .nav {
        float: right;
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
