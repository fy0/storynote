<template>
<div class="">
    <h3 class="">新建主题</h3>
    <form class="pure-form" id="form_topic" method="POST" @submit="send">
        <fieldset>
            <div class="">
                <input type="text" name="title" placeholder="这里填写标题，最长50个字" style="width: 100%">
            </div>
            <div class="">
                <textarea style="width:100%" rows="15" id="editor" name="content" placeholder="这里填写内容 ..." autofocus></textarea>
            </div>
            <div class="">
                <button class="pure-button pure-button-primary">发布</button>
            </div>
        </fieldset>
    </form>
</div>
</template>

<script>

export default {
    data () {
        return {
            msg: 'Hello Vue 2.0!'
        }
    },
    methods: {
        send: function (e) {
            console.log(12312321);
            console.log($("#form_topic"))
            //for (let i of a.entries()) {b[i[0]] = b[i[1]];}
        }
    }
}
</script>

<style>

</style>
