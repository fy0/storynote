<template>
<div v-if="page_info.items">
    <div class="topic-item" v-for="item in page_info.items" :key="item.id">
        <h3 class="title">
            <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
        </h3>
        <div class="brief" v-html="marked(item.brief)"></div>
        <small><router-link :to="{ path: '/t/' + item.id }">阅读原文</router-link></small>
        <p class="info">由 {{item.user.name}} 发表于 {{time_to_text(item.time)}}</p>
        <div class="divider-line"></div>
    </div>
    <ul class="ic-pages">
        <li v-if="page_info.first_page">
            <router-link :to="{ path: `/p/${page_info.first_page}` }" class="slim">«</router-link>
        </li>

        <li v-if="page_info.prev_page">
            <router-link :to="{ path: `/p/${page_info.prev_page}` }" class="slim">‹</router-link>
        </li>
        <li v-else><a href="javascript:void(0);" class="disable slim">‹</a></li>

        <li v-for="i in page_info.page_numbers" :key="i">
            <router-link :to="{ path: `/p/${i}` }" :class="(page_info.cur_page == i) ? 'active' : ''">{{i}}</router-link>
        </li>

        <li v-if="page_info.next_page">
            <router-link :to="{ path: `/p/${page_info.next_page}` }" class="slim">›</router-link>
        </li>
        <li v-else><a href="javascript:void(0);" class="disable slim">›</a></li>
        
        <li v-if="page_info.last_page">
            <router-link :to="{ path: `/p/${page_info.last_page}` }" class="slim">»</router-link>
        </li>
    </ul>
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
    components: {
        Loading,
    }
}
</script>
