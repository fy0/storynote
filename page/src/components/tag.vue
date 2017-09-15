<template>
<div v-if="page_info">
    <div class="tagtitle">标签：<span>{{tagname}}</span></div>
    <div v-if="page_info.items">
        <TopicItem v-for="item in page_info.items" :item="item.data" :key="item.id"></TopicItem>
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
import TopicItem from "./utils/topic_item.vue"

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
        TopicItem
    }
}
</script>
