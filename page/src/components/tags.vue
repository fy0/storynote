<template>
<div>
    <h4>标签列表</h4>
    <p v-for="tag in page_info" :key="tag.id">
        <router-link :to="{ name: 'tag', params: {name: tag.name}}">{{tag.name}}</router-link>    
    </p>
</div>
</template>

<style>
</style>

<script>
import api from "../netapi.js"

export default {
    data () {
        return {
            page_info: null
        }
    },
    mounted: async function () {
        let ret = await api.tagList();
        this.$set(this, "page_info", ret.data);
    },
}
</script>
