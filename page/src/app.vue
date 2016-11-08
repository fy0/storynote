<template>
<div id="app">
    <div class="ic-container">
        <router-view></router-view>
    </div>
    <msg-tip></msg-tip>
</div>
</template>

<script>
import MsgTip from './components/msgtip.vue'
export default {
    data () {
        return {
        }
    },
    components: {
        // <my-component> 将只在父模板可用
        'msg-tip': MsgTip
    }
}
</script>

<style>

</style>
