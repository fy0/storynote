<template>
<div class="">
    <h3 class="">新建主题</h3>
    <form class="pure-form" id="form_topic" method="POST" @submit.prevent="send">
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

import api from "../netapi.js"
import SimpleMDE from "simplemde"

export default {
    data () {
        return {
            msg: 'Hello Vue 2.0!'
        }
    },
    methods: {
        send: async function (e) {
            let formdata = new FormData($("#form_topic")[0]);
            //for (let i of formdata.entries()) { data[i[0]] = i[1]; }
            let title = (formdata.get("title") || "").trim();
            let content = this.editor.value();

            if (!title) {
                //$.messages_error('请至少输入一个标题！');
                return false;
            }

            if (title.length < 5) {
                //$.messages_error('标题应不少于 5 个字！');
                return false;
            }

            if (title.length > 30) {
                //$.messages_error('标题应不多于 30 个字！');
                return false;
            }

            if (!content) return;
            api.topicNew(title, content);
            alert("OK!");
        }
    },
    mounted: function () {
        this.editor = new SimpleMDE({
            element: document.getElementById("editor"),
            spellChecker: false,
            autoDownloadFontAwesome: true,
            autosave: {
                enabled: true,
                unique_id: "editor",
            },
            renderingConfig: {
                singleLineBreaks: false,
                codeSyntaxHighlighting: true,
            },
        });
    }
}
</script>

<style>

</style>
