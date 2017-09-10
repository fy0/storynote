<template>
<div v-if="page_info">
    <div class="tagtitle">标签：<span>{{tagname}}</span></div>
    <div v-if="page_info.items">
        <div class="topic-item" v-for="item in page_info.items" :key="item.data.id">
            <h3 class="title">
                <router-link :to="{ path: '/t/' + item.data.id }">{{item.data.title}}</router-link>
            </h3>
            <div class="brief" v-html="marked_brief(item.data.brief)"></div>
            <span class="topic-link"><router-link :to="{ path: '/t/' + item.data.id }">阅读全文</router-link></span>
            <p class="info">由 {{item.data.user.name}} 发表于 {{time_to_text(item.data.time)}} / 翻阅 {{item.data.view_count}}</p>
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
    <div v-else>无此标签数据</div>
</div>
<loading v-else></loading>
</template>

<style scoped>
.tagtitle {
    margin-top: 20px;
}
</style>

<script>
import Vue from 'vue'
import api from "../netapi.js"
import state from "../state.js"
import Loading from "./utils/loading.vue"

export default {
    data () {
        return {
            exists: false,
            page_info: null,
            state: state,
        }
    },
    methods: {
        marked_brief: $.marked_brief,
        time_to_text: $.time_to_text,
    },
    computed: {
        tagname: function () {
            return this.$route.params.name;
        }
    },
    mounted: async function () {
    },
    beforeRouteEnter: async (to, from, next) => {
        let name = to.params.name;
        let ret = await api.tagGetTopics(name);

        if (ret.code == api.retcode.SUCCESS) {
            return next(vm => {
                vm.page_info = ret.data;
            });
        } else if (ret.code == api.retcode.NOT_FOUND) {
            return next(vm => {
                vm.page_info = {}
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
