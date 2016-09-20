<template>
<div>
    <div class="topic-content entry">
        <div class="content" v-if="topic">
            <h1 class="post-title">{{topic.title}}</h1>
            <div class="post-info">
                <span>{{topic.user.name}}</span>
                <span>{{getTime(topic.time)}}</span>
            </div>
            <div v-html="topic.content"></div>
        </div>
    </div>
</div>
</template>

<style>
.post-title {
    margin: 0.3em 0;
}
.post-info {
    color: rgb(153, 153, 153);
    padding: 10px 0px;
    font-size: small;
}
</style>

<script>
import api from "../netapi.js"

export default {
    data () {
        return {
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
            console.log(ret);
            this.$set(this, "topic", ret.data);
        }
    }
}
</script>

<style>

</style>
