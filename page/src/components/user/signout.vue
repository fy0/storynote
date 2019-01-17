<template>
<div></div>
</template>

<style>
</style>

<script>
import api from '../../netapi.js'

export default {
    data () {
        return {}
    },
    head () {
        return {
            title: `登出`
        }
    },
    mounted: async function () {
        await api.userSignout()
        this.$store.commit('SET_USERDATA', null)
        this.$router.replace('/')
        $.message_success(`您已成功注销`)
    }
}
</script>
