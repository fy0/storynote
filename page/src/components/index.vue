<template>
<div>
    <div class="nav" v-if="state.data.user">
        <a href="#">标签</a>
        <a href="#">文章</a>
        <a href="#">项目</a>
        <router-link :to="{ path: '/new' }">新建</router-link>
    </div>
    <h1>SinglePage</h1>
    <div class="pure-g">
        <div class="pure-u-3-4">
            <div v-if="page_info.items">
                <div class="topic-item" v-for="item in page_info.items">
                    <p class="title">
                        <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
                    </p>
                    <p class="info">{{time_to_text(item.time)}}</p>
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

<style>
.topic-item > .title {

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
        let ret = await api.topicRecent();
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
