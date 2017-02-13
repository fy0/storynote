<template>
<div class="topic-content entry">
    <div class="content" v-if="topic">
        <h1 class="post-title">{{topic.title}}</h1>
        <div class="post-info">
            <span>{{topic.user.name}}</span>
            <span>{{getTime(topic.time)}}</span>
        </div>
        <div v-html="marked(topic.content)"></div>
    </div>
    <loading v-else></loading>
</div>
</template>

<style>
.post-title {
    word-wrap: break-word;
    margin: 0.3em 0 0;
}
.post-info {
    color: rgb(153, 153, 153);
    padding: 0px;
    font-size: small;
}
</style>

<script>
import marked from "marked"
import api from "../netapi.js"
import Loading from "./loading.vue"

export default {
    data () {
        return {
            marked,
            topic: null,
        }
    },
    methods: {
        getTime: (timestamp) => {
            return $.get_time(timestamp);
        }
    },
    mounted: async function () {
        let ret = await api.topicGet(this.$route.params.id);
        if (ret.code == 0) {
            this.$set(this, "topic", ret.data);
        }
    },
    components: {
        Loading,
    }
}
</script>

<style>

</style>
