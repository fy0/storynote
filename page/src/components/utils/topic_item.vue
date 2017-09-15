<template>
<div class="topic-item">
    <h3 class="title">
        <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
    </h3>
    <div class="brief" v-html="marked_brief(item.brief)"></div>
    <span class="topic-link"><router-link :to="{ path: '/t/' + item.id }">阅读全文</router-link></span>
    <p class="info">由 {{item.user.name}} 发表于 {{time_to_text(item.time)}} / 翻阅 {{item.view_count}}</p>
    <div class="divider-line"></div>
</div>
</template>

<style>
</style>

<script>
import state from "../../state.js"

export default {
    props: {
        item: Object,
    },
    data () {
        return {
            state,
        }
    },
    methods: {
        marked_brief: $.marked_brief,
        time_to_text: $.time_to_text,
    }
}
</script>
