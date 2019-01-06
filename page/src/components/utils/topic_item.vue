<template>
<div class="topic-item">
    <h3 class="title">
        <span v-if="item.link_to">[引用]</span>
        <span v-if="item.state != aaa.misc.TOPIC_STATE.NORMAL">[{{aaa.misc.TOPIC_STATE_TXT[item.state]}}]</span>
        <a class="ref-topic" target="_blank" :href="item.link_to" v-if="item.link_to">{{item.title}}</a>
        <router-link v-else :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
    </h3>
    <div class="brief" v-html="marked_brief(item.brief)"></div>
    <span class="topic-link"><router-link :to="{ path: '/t/' + item.id }">{{item.link_to ? '发表评论' : '阅读全文'}}</router-link></span>
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
import state from '../../state.js'
import api from '@/netapi.js'

export default {
    props: {
        item: Object
    },
    data () {
        console.debug(3333333333, {})
        return {
            aaa: null,
            state
        }
    },
    async asyncData () {
        if (!state.data.misc) {
            let ret = await api.misc()
            Vue.set(state.data, 'misc', ret.data)
        }
            let ret = await api.misc()
            this.aaa = {}
            Vue.set(this.aaa, 'misc', ret.data)
            console.debug(444444)

            ret = await api.userInfo()
            if (ret.code === 0) {
                Vue.set(state.data, 'user', ret.data)
            }
        console.debug(444433, {})
        return {}
    },
    created: async function () {
        console.debug(3333333333)
        // if (!this.state.data.misc) {
            let ret = await api.misc()
            this.aaa = {}
            Vue.set(this.aaa, 'misc', ret.data)
            console.debug(444444)

            ret = await api.userInfo()
            if (ret.code === 0) {
                Vue.set(state.data, 'user', ret.data)
            }
        // }
    },
    methods: {
        marked_brief: $.marked_brief,
        time_to_text: $.time_to_text
    }
}
</script>
