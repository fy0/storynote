<template>
<div class="tmp">
    <div class="pure-g" v-for="key in info.key_order" :key="key">
        <div class="pure-u-2-24 timeline-tag">
            <span>{{key}}</span>
            <!--<span class="vline"></span>-->
        </div>
        <div class="pure-u-22-24">
            <TopicItem v-for="item in info.timeline[key]" :item="item" :key="item.id"></TopicItem>
        </div>
    </div>

    <paginator :page-info='info.data' :route-name='"timeline"'></paginator>
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
</style>

<script>
import Vue from 'vue'
import api from "../netapi.js"
import state from "../state.js"
import Loading from "./utils/loading.vue"
import Paginator from "./utils/paginator.vue"
import TopicItem from "./utils/topic_item.vue"

export default {
    data () {
        return {
            state,
            info: {},
        }
    },
    methods: {
        marked_brief: $.marked_brief,
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
    beforeRouteUpdate: async function (to, from, next) {
        let page = to.params.page;
        let ret = await api.timeline(page);

        if (ret.code == api.retcode.SUCCESS) {
            this.info = ret;
            return next();
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`);
        return next('/');
    },
    components: {
        Loading,
        Paginator,
        TopicItem
    }
}
</script>
