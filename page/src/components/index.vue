<template>
<div>
    <TopicItem v-for="item in page_info.items" :item="item" :key="item.id"></TopicItem>
    <paginator :page-info='page_info' :route-name='"index"'></paginator>
</div>
</template>

<style>
/*.tmp {
    max-height: 70vh;
    overflow-y: scroll;
}*/
</style>

<script>
import Vue from 'vue'
import {marked} from '../md.js'
import api from "../netapi.js"
import state from "../state.js"
import Paginator from "./utils/paginator.vue"
import TopicItem from "./utils/topic_item.vue"

export default {
    data () {
        return {
            page_info: {},
            state: state,
        }
    },
    methods: {
        marked_brief: $.marked_brief,
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
        Paginator,
        TopicItem
    }
}
</script>
