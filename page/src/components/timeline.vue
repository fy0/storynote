<template>
<div class="tmp" v-if="page_info">
    <div class="pure-g" v-for="key in page_info.key_order">
        <div class="pure-u-2-24 timeline-tag">
            <span>{{key}}</span>
        </div>
        <div class="pure-u-22-24">
            <div class="topic-item" v-for="item in page_info.timeline[key]">
                <h3 class="title">
                    <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
                </h3>
                <div class="brief" v-html="marked(item.brief)"></div>
                <small><router-link :to="{ path: '/t/' + item.id }">阅读原文</router-link></small>
                <p class="info">由 {{item.user.name}} 发表于 {{time_to_text(item.time)}}</p>
                <div class="divider-line"></div>
            </div>
        </div>
    </div>
</div>
<loading v-else></loading>
</template>

<style>
/*.tmp {
    max-height: 70vh;
    overflow-y: scroll;
}*/

.timeline-tag {
    margin-top: 20px;
}

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
import Loading from "./loading.vue"

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
            let ret = await api.timeline(page);
            console.log(ret, ret.key_order);
            this.$set(this, "page_info", ret);
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
