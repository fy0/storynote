<template>
<div>
    <div class="topic-item" v-for="item in page_info.items" :key="item.id">
        <h3 class="title">
            <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
        </h3>
        <div class="brief" v-html="marked(item.brief)"></div>
        <small><router-link :to="{ path: '/t/' + item.id }">阅读原文</router-link></small>
        <p class="info">由 {{item.user.name}} 发表于 {{time_to_text(item.time)}} / 翻阅 {{item.view_count}}</p>
        <div class="divider-line"></div>
    </div>
    <paginator :page-info='page_info' :route-name='"index"'></paginator>
</div>
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
import Paginator from "./utils/paginator.vue"

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
    },
    mounted: async function () {
    },
    beforeRouteEnter: async (to, from, next) => {
        let page = to.params.page;
        let ret = await api.recent(page);

        if (ret.code == api.retcode.SUCCESS) {
            return next(vm => {
                vm.page_info = ret.data;
            });
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`);
        return next('/');
    },
    beforeRouteUpdate: async function (to, from, next) {
        let page = to.params.page;
        let ret = await api.recent(page);

        if (ret.code == api.retcode.SUCCESS) {
            this.page_info = ret.data;
            return next();
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`);
        return next('/');
    },
    components: {
        Paginator
    }
}
</script>
