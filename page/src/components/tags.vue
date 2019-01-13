<template>
<div>
    <h3>标签列表</h3>
    <p v-for="tag in page_info" :key="tag.id">
        <nuxt-link :to="{ name: 'tag', params: {name: tag.name}}">{{tag.name}}</nuxt-link>
    </p>
</div>
</template>

<style>
</style>

<script>
import api from '../netapi.js'

export default {
    data () {
        return {
            page_info: null
        }
    },
    head () {
        return {
            title: `标签列表`,
            meta: [
                // hid is used as unique identifier. Do not use `vmid` for it as it will not work
                // { hid: 'description', name: 'description', content: 'My custom description' }
            ]
        }
    },
    mounted: async function () {
    },
    beforeRouteEnter: async (to, from, next) => {
        let ret = await api.tagList()

        if (ret.code === api.retcode.SUCCESS) {
            return next(vm => {
                vm.page_info = ret.data
            })
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`)
        return next('/')
    }
}
</script>
