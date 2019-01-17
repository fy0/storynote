<template>
<div class="topic-item">
    <h3 class="title">
        <span v-if="item.link_to">[引用]</span>
        <span v-if="item.state != $store.state.misc.TOPIC_STATE.NORMAL">[{{$store.state.misc.TOPIC_STATE_TXT[item.state]}}]</span>
        <a class="ref-topic" target="_blank" :href="item.link_to" v-if="item.link_to">{{item.title}}</a>
        <nuxt-link v-else :to="{ path: '/t/' + item.id }">{{item.title}}</nuxt-link>
    </h3>
    <div class="brief" v-html="marked_brief(item.brief)"></div>
    <span class="topic-link"><nuxt-link :to="{ path: '/t/' + item.id }">{{item.link_to ? '发表评论' : '阅读全文'}}</nuxt-link></span>
    <p class="info">由 {{item.user.name}} 发表于 {{time_to_text(item.time)}} / 翻阅 {{item.view_count}}</p>
    <div class="divider-line"></div>
</div>
</template>

<style>
.ref-topic {
    color: #219787;
}
</style>

<script>
// import api from '@/netapi.js'

export default {
    props: {
        item: Object
    },
    data () {
        return {
        }
    },
    created: async function () {
    },
    methods: {
        marked_brief: $.marked_brief,
        time_to_text: $.time_to_text
    }
}
</script>
