<template>
<div class="tmp" v-if="page_info.items">
    <div class="topic-item" v-for="item in page_info.items">
        <h3 class="title">
            <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
        </h3>
        <div class="brief" v-html="marked(item.brief)"></div>
        <small><router-link :to="{ path: '/t/' + item.id }">阅读原文</router-link></small>
        <p class="info">由 {{item.user.name}} 发表于 {{time_to_text(item.time)}}</p>
        <div class="divider-line"></div>
    </div>
    <span v-if="page_info.prev_page">
        <router-link :to="{ path: `/p/${page_info.prev_page}` }">上一页</router-link>
    </span>
    <span v-if="page_info.next_page">
        <router-link :to="{ path: `/p/${page_info.next_page}` }">下一页</router-link>
    </span>
</div>
<loading v-else></loading>
</template>

<style>
/*.tmp {
    max-height: 70vh;
    overflow-y: scroll;
}*/
.topic-item {}

.topic-item > .title {
    font-weight: normal;
    margin-bottom: 0;
}

.topic-item > .info {
    color: rgb(153, 153, 153);
    font-size: small;
}

.topic-item > .brief {
    max-height: 200px;
    overflow: hidden;
}
</style>

<script>
import Vue from 'vue'
import marked from 'marked'
import api from "../netapi.js"
import state from "../state.js"
import Loading from "./utils/loading.vue"

export default {
    data () {
        return {
            page_info: {},
            state: state,
        }
    },
    methods: {
        marked,
        time_to_text: $.time_to_text,
        fetchData: async function (page) {
            let ret = await api.recent(page);
            //console.log(ret);
            this.$set(this, "page_info", ret.data);
        }
    },
    mounted: async function () {
        this.fetchData(this.$route.params.page);
    },
    watch: {
        '$route' (to, from) {
            this.fetchData(to.params.page);
        }
    },
    components: {
        Loading,
    }
}
</script>
