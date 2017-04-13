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
import state from "../state.js"
import SimpleMDE from "simplemde"
import Prism from "prismjs"

export default {
    data () {
        return {
        }
    },
    methods: {
        send: async function (e) {
            let formdata = new FormData($("#form_topic")[0]);
            let title = (formdata.get("title") || "").trim();
            let content = this.editor.value();

            if (!title) {
                 $.message_error('请至少输入一个标题！');
                return false;
            }

            if (title.length < 5) {
                $.message_error('标题应不少于 5 个字！');
                return false;
            }

            if (title.length > 30) {
                $.message_error('标题应不多于 30 个字！');
                return false;
            }

            if (!content) return;
            let ret = await api.topicNew(title, content);
            if (ret.code == 0) {
                this.$router.push({ name: 'topic1', params: { id: ret.data.id }})
                $.message_success('发表成功！已自动跳转至文章页面。');
            } else {
                $.message_error('发表失败！');                
            }
        }
    },
    mounted: function () {
        this.editor = new SimpleMDE({
            element: document.getElementById("editor"),
            spellChecker: false,
            autoDownloadFontAwesome: false,
            autosave: {
                enabled: true,
                unique_id: "editor",
            },
            renderingConfig: {
                singleLineBreaks: false,
                codeSyntaxHighlighting: false,
            },
            previewRender: function (plainText, preview) { // Async method
                setTimeout(function () {
                    preview.innerHTML = this.parent.markdown(plainText);
                    Prism.highlightAll();
                }.bind(this), 1);
                return "Loading...";
            },
        });
    },
    beforeRouteEnter: (to, from, next) => {
        if (!state.data.user) {
            return;
        }
        next();
    }
}
</script>

<style>

</style>
