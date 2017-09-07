<template>
<div class="tmp">
    <div class="pure-g" v-for="key in info.key_order" :key="key">
        <div class="pure-u-2-24 timeline-tag">
            <span>{{key}}</span>
            <!--<span class="vline"></span>-->
        </div>
        <div class="pure-u-22-24">
            <div class="topic-item" v-for="item in info.timeline[key]" :key="item.id">
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

    <div class="ic-pages" v-if="info.data.last_page == info.data.first_page">
        <span v-if="info.data && info.data.prev_page">
            <router-link :to="{ path: `/timeline/${info.data.prev_page}` }">上一页</router-link>
        </span>
        <span v-if="info.data && info.data.next_page">
            <router-link :to="{ path: `/timeline/${info.data.next_page}` }">下一页</router-link>
        </span>
    </div>
</div>
</template>

<style>
/*.tmp {
    max-height: 70vh;
    overflow-y: scroll;
}*/

.timeline-tag {
    margin-top: 20px;
}

.timeline-tag > .vline {
    display: block;
    border-left: 1px solid #ccc;
    height: 98%;
    width: 0px;
    margin-left: 1.5em;
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
import Loading from "./utils/loading.vue"

export default {
    data () {
        return {
            state,
            info: {},
        }
    },
    methods: {
        marked,
        time_to_text: $.time_to_text,
    },
    mounted: async function () {
        // this.fetchData(this.$route.params.page);
    },
    beforeRouteEnter: async (to, from, next) => {
        let page = to.params.page;
        let ret = await api.timeline(page);

        if (ret.code == api.retcode.SUCCESS) {
            return next(vm => {
                vm.info = ret;
            });
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`);
        return next('/');
    },
    components: {
        Loading,
    }
}
</script>
