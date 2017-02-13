<template>
<div v-if="page_info.items">
    <div class="topic-item" v-for="item in page_info.items">
        <h3 class="title">
            <router-link :to="{ path: '/t/' + item.id }">{{item.title}}</router-link>
        </h3>
        <p class="info">{{time_to_text(item.time)}}</p>
        <div class="divider-line"></div>
    </div>
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
    },
    mounted: async function () {
        let ret = await api.recent();
        //console.log(ret);
        this.$set(this, "page_info", ret.data);
    },
    components: {
        Loading,
    }
}
</script>
