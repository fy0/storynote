<template>
<div>
    <h3>标签列表</h3>
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
    },
    beforeRouteEnter: async (to, from, next) => {
        let ret = await api.tagList();

        if (ret.code == api.retcode.SUCCESS) {
            return next(vm => {
                vm.page_info = ret.data;
            });
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`);
        return next('/');
    },
}
</script>
