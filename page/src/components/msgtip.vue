<template>
<div class="tipbox">
    <div class="item" v-for="item in messages" @click.stop="openFile(item)">
        <a>{{item.title}}</a><br />
    </div>
    <router-link :to="{ path: '/' }">Go to Index</router-link>
</div>
</template>

<style>
    $blue: #056ef0;

    .tipbox {
        position: fixed;
        left: 0;
        bottom: 5%;
        color: $blue;

        .item {
            padding-left: 10px;
            color: red;
        }
    }
</style>

<script>
export default {
    data () {
        return {
            messages: [
                {title: '测试'},
            ],
        }
    }
}
</script>

<style>

</style>
