<template>
<div class="">
    <h3 class="">新建主题</h3>
    <form class="pure-form" id="form_topic" method="POST" @submit.prevent="send">
        <fieldset>
            <div class="form-item">
                <input type="text" name="title" placeholder="这里填写标题，最长50个字" style="width: 72%; font-size: 15px; font-weight: bolder;">
                <el-date-picker
                    style="width: 27%; margin-top: -0.3px;"
                    v-model="date"
                    type="datetime"
                    placeholder="选择日期时间"
                    align="left"
                    :picker-options="pickerOptions">
                </el-date-picker>
            </div>
            <div class="form-item">
            </div>
            <div class="form-item">
                <textarea style="width:100%" rows="15" id="editor" name="content" placeholder="这里填写内容 ..." autofocus></textarea>
            </div>
            <div class="form-item">
                <el-button style="float: right" type="primary" @click="send">发布</el-button>
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
            date: new Date(),
            pickerOptions: {
                shortcuts: [{
                    text: '当前',
                    onClick(picker) {
                        picker.$emit('pick', new Date());
                    }
                }, {
                    text: '昨天',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24);
                        picker.$emit('pick', date);
                    }
                }, {
                    text: '一周前',
                    onClick(picker) {
                        const date = new Date();
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                        picker.$emit('pick', date);
                    }
                }]
            },
        }
    },
    methods: {
        send: async function (e) {
            let formdata = new FormData($("#form_topic")[0]);
            let title = (formdata.get("title") || "").trim();
            let content = this.editor.value();

            if (!title) {
                 $.message_error('请输入一个标题！');
                return false;
            }

            if (title.length < state.data.misc.TITLE_LENGTH_MIN) {
                $.message_error(`标题应不少于 ${state.data.misc.TITLE_LENGTH_MIN} 个字！`);
                return false;
            }

            if (title.length > state.data.misc.TITLE_LENGTH_MAX) {
                $.message_error(`标题应不多于 ${TITLE_LENGTH_MAX} 个字！`);
                return false;
            }

            let postTime = parseInt(this.date.getTime() / 1000);

            if (!content) return;
            let ret = await api.topicNew(title, content, postTime);
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
            $.message_error('抱歉，无权访问此页面');
            next('/');
            return;
        }
        next();
    }
}
</script>

<style>
.form-item {
    margin-bottom: 10px;
}
</style>
