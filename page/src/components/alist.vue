<template>
<div>
    <div class="item" v-for="item in articles" @click.stop="openFile(item)">
        <a>{{item.title}}</a><br />
        <router-link :to="{ path: '/foo' }">Go to Foo</router-link>
    </div>
</div>
</template>

<script>
export default {
    data () {
        return {
            articles: [
                {title: '测试'},
            ],
            msg: 'Hello Vue 2.0!'
        }
    }
}
</script>

<style>

</style>
