<template>
<ul class="ic-pages" v-if="pageInfo && pageInfo.page_count > 1">
   <li v-if="pageInfo.first_page">
        <nuxt-link :to="toInfo(pageInfo.first_page)" class="slim">«</nuxt-link>
    </li>

    <li v-if="pageInfo.prev_page">
        <nuxt-link :to="toInfo(pageInfo.prev_page)" class="slim">‹</nuxt-link>
    </li>
    <li v-else><a href="javascript:void(0);" class="disable slim">‹</a></li>

    <li v-for="i in pageInfo.page_numbers" :key="i">
        <nuxt-link :to="toInfo(i)" :class="(pageInfo.cur_page === i) ? 'active' : ''">{{i}}</nuxt-link>
    </li>

    <li v-if="pageInfo.next_page">
        <nuxt-link :to="toInfo(pageInfo.next_page)" class="slim">›</nuxt-link>
    </li>
    <li v-else><a href="javascript:void(0);" class="disable slim">›</a></li>

    <li v-if="pageInfo.last_page">
        <nuxt-link :to="toInfo(pageInfo.last_page)" class="slim">»</nuxt-link>
    </li>
</ul>
</template>

<style>
</style>

<script>
import state from '../../state.js'

export default {
    props: {
        pageInfo: Object,
        routeName: String,
        pageKey: {
            type: String,
            default: 'page'
        }
    },
    data () {
        return {
            state
        }
    },
    methods: {
        toInfo: function (page) {
            return {
                name: this.routeName,
                params: {
                    p: 'p',
                    [this.pageKey]: page
                }
            }
        }
    }
}
</script>
