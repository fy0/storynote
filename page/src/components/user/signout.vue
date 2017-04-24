<template>
</template>

<style>
</style>

<script>
import Vue from 'vue'
import api from "../../netapi.js"
import state from "../../state.js"

export default {
    data () {
        return {}
    },
    mounted: async function () {
        let ret = await api.userSignout();
        Vue.delete(state.data, 'user');
        this.$router.replace('/');
        $.message_success(`您已成功注销`);
    }
}
</script>
