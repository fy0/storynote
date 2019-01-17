<template>
<div class="tmp">
    <div class="tl-item" v-for="key in info.key_order" :key="key">
        <div class="tl-tag">
            <span>{{key}}</span>
            <!--<span class="vline"></span>-->
        </div>
        <div class="info">
            <TopicItem v-for="item in info.timeline[key]" :item="item" :key="item.id"></TopicItem>
        </div>
    </div>

    <paginator :page-info='info.data' :route-name='"timeline"'></paginator>
</div>
</template>

<style lang="scss">
.tl-item {
    display: flex;

    > .tl-tag {
        flex: 2 0 0%;
        width: 0%;
        margin-top: 20px;
    }

    > .info {
        flex: 22 0 0%;
        width: 0%;
        word-break: break-all;
    }
}

.tl-tag > .vline {
    display: block;
    border-left: 1px solid #ccc;
    height: 98%;
    width: 0px;
    margin-left: 1.5em;
}
</style>

<script>
import api from '../netapi.js'
import Paginator from './utils/paginator.vue'
import TopicItem from './utils/topic_item.vue'

export default {
    data () {
        return {
            info: {}
        }
    },
    head () {
        return {
            title: '时间线',
            meta: [
                // hid is used as unique identifier. Do not use `vmid` for it as it will not work
                // { hid: 'description', name: 'description', content: 'My custom description' }
            ]
        }
    },
    methods: {
        marked_brief: $.marked_brief,
        time_to_text: $.time_to_text
    },
    mounted: async function () {
        // this.fetchData(this.$route.params.page);
    },
    beforeRouteEnter: async (to, from, next) => {
        let page = to.params.page
        let ret = await api.timeline(page)

        if (ret.code === api.retcode.SUCCESS) {
            return next(vm => {
                vm.info = ret
            })
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`)
        return next('/')
    },
    beforeRouteUpdate: async function (to, from, next) {
        let page = to.params.page
        let ret = await api.timeline(page)

        if (ret.code === api.retcode.SUCCESS) {
            this.info = ret
            return next()
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`)
        return next('/')
    },
    components: {
        Paginator,
        TopicItem
    }
}
</script>
