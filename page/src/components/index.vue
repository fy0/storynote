<template>
<div v-if="page_info.items">
    <div class="topic-item" v-for="item in page_info.items">
        <h3 class="title">
            <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
        </h3>
        <p class="info">{{time_to_text(item.time)}}</p>
        <div class="divider-line"></div>
    </div>
    <span v-if="page_info.prev_page">
        <router-link :to="{ path: `/p/${page_info.prev_page}` }">上一页</router-link>
    </span>
    <span v-if="page_info.next_page">
        <router-link :to="{ path: `/p/${page_info.next_page}` }">下一页</router-link>
    </span>
</div>
<loading v-else></loading>
</template>

<style>
.topic-item {}

.topic-item > .title {
    font-weight: normal;
}

.topic-item > .info {
    color: rgb(153, 153, 153);
    font-size: small;
}

.divider-line {
    border-bottom: #EBF2F6 1px solid;
    width: 50%;
}
</style>

<script>
import Vue from 'vue'
import api from "../netapi.js"
import state from "../state.js"
import Loading from "./loading.vue"

export default {
    data () {
        return {
            page_info: {},
            state: state,
        }
    },
    methods: {
        time_to_text: $.time_to_text,
        fetchData: async function (page) {
            let ret = await api.recent(page);
            //console.log(ret);
            this.$set(this, "page_info", ret.data);
        }
    },
    mounted: async function () {
        this.fetchData(this.$route.params.page);
    },
    watch: {
        '$route' (to, from) {
            this.fetchData(to.params.page);
        }
    },
    components: {
        Loading,
    }
}
</script>
