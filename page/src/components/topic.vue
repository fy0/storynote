<template>
<div>
    <div class="topic-content entry">
        <div class="content" v-if="topic">
            <h1>{{topic.title}}</h1>
            <div v-html="topic.content"></div>
        </div>
        123123
    </div>
</div>
</template>

<script>
import api from "../netapi.js"

export default {
    data () {
        return {
            topic: null,
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
