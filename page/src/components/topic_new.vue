<template>
<div class="">
    <div class="edit-page-title">
        <h3 class="" v-if="!is_edit">新建主题</h3>
        <h3 class="" v-else>编辑主题</h3>
        <el-button class="right-top-btn" type="primary" :loading="loading" @click="send">{{postButtonText}}</el-button>
    </div>

    <form class="pure-form" id="form_topic" method="POST" @submit.prevent="send">
        <fieldset>
            <div class="form-item">
                <input type="text" name="title" v-model="topicInfo.title" placeholder="这里填写标题，最长50个字" style="width: 72%; font-size: 15px; font-weight: bolder;">
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
                <input type="text" name="link_to" v-model="topicInfo.link_to" placeholder="填写外站引用链地址 (可选)" style="width: 72%; font-size: 15px; font-weight: bolder;">
                <el-select v-model="topicInfo.state" placeholder="请选择" style="width: 27%; font-size: 15px; font-weight: bolder;">
                    <el-option v-for="[v, k] in topicStateOptions" :key="parseInt(v)" :label="`状态：${k}`" :value="parseInt(v)"></el-option>
                </el-select>
            </div>
            <div class="form-item">
                <markdown-editor :configs="mdeConfig" v-model="topicInfo.content" placeholder="这里填写内容 ..." rows="15" autofocus></markdown-editor>
            </div>
            <div class="form-item">
                <el-button style="float: right" type="primary" :loading="loading" @click="send">{{postButtonText}}</el-button>
            </div>
        </fieldset>
    </form>

    <form method="post" action="http://upload.qiniu.com/" enctype="multipart/form-data">
    <input name="token" type="hidden" :value="token">
    <input name="file" type="file" />
    <input name="accept" type="hidden" />
    <input type="submit" />
    </form>

</div>
</template>


<style>
.edit-page-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.edit-page-title > h3 {
}

.right-top-btn {
}

.form-item {
    margin-bottom: 10px;
}

.el-select > .el-input > input[readonly] {
    background-color: #fff;
    color: #1f2d3d;    
}
</style>


<script>
import api from "../netapi.js"
import state from "../state.js"
import markdownEditor from 'vue-simplemde/src/markdown-editor.vue'
import 'simplemde/dist/simplemde.min.css'
import Prism from "prismjs"

export default {
    data () {
        return {
            loading: false,
            date: new Date(),

            topicInfo: {
                title: '',
                link_to: '',
                state: state.data.misc.TOPIC_STATE.NORMAL,
                board: null,
                content: ''
            },

            token: '',
            
            mdeConfig: {
                spellChecker: false,
                autoDownloadFontAwesome: false,
                autosave: {
                    enabled: false,
                    uniqueId: 'topic-post-content'
                },
                renderingConfig: {
                    singleLineBreaks: false,
                    codeSyntaxHighlighting: false
                },
                previewRender: function (plainText, preview) { // Async method
                    setTimeout(function () {
                        preview.innerHTML = this.parent.markdown(plainText)
                        Prism.highlightAll()
                    }.bind(this), 1)
                    return 'Loading...'
                }
            },

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
    computed: {
        topicStateOptions: function () {
            return Object.entries(state.data.misc.TOPIC_STATE_TXT);
        },
        is_edit () {
            return this.$route.name == 'topic_edit'
        },
        postButtonText: function () {
            return this.loading ? '请等待' 
                : (this.is_edit ? '编辑' : '发布');
        }
    },
    methods: {
        send: async function (e) {
            if (!this.topicInfo.title) {
                $.message_error('请输入一个标题！');
                return false;
            }

            if (this.topicInfo.title.length < state.data.misc.TITLE_LENGTH_MIN) {
                $.message_error(`标题应不少于 ${state.data.misc.TITLE_LENGTH_MIN} 个字！`);
                return false;
            }

            if (this.topicInfo.title.length > state.data.misc.TITLE_LENGTH_MAX) {
                $.message_error(`标题应不多于 ${TITLE_LENGTH_MAX} 个字！`);
                return false;
            }

            this.topicInfo.time = parseInt(this.date.getTime() / 1000);

            // 允许页面内容为空
            // if (!content) return;

            let ret;
            let success_text;
            let failed_text;

            this.loading = true;
            if (this.is_edit) {
                ret = await api.topicEdit(this.$route.params.id, this.topicInfo);
                success_text = '编辑成功！已自动跳转至文章页面。';
                failed_text = ret.msg || '编辑失败！';
            } else {
                ret = await api.topicNew(this.topicInfo);
                success_text = '发表成功！已自动跳转至文章页面。';
                failed_text = ret.msg || '编辑失败！';
            }
    
            if (ret.code == 0) {
                localStorage.setItem('topic-post-cache-clear', 1);
                this.$router.push({ name: 'topic', params: { id: ret.data.id }})
                $.message_success(success_text);
            } else {
                $.message_error(failed_text);
                // 注意：发布成功会跳转，故不做复位，失败则复位
                this.loading = false;
            }
        }
    },
    mounted: async function () {
        let ret = await api.qn();
        this.token = ret.data;

        if (localStorage.getItem('topic-post-cache-clear')) {
            // 我不知道为什么，在地址跳转前进行 storage 的清除工作，
            // 并不会实质上起效，因此这是一个替代手段，效果比较理想。
            localStorage.removeItem('topic-post-title');
            localStorage.removeItem('smde_topic-post-content');
            localStorage.removeItem('topic-post-cache-clear');
        }

        if (!this.is_edit) {
            this.title = localStorage.getItem('topic-post-title') || '';
        }
    },
    watch: {
        title: _.debounce(function (val, oldVal) {
            localStorage.setItem('topic-post-title', val);
        }, 5000),
    },
    beforeRouteEnter: async (to, from, next) => {
        if (!state.data.user) {
            $.message_error('抱歉，无权访问此页面');
            return next('/')
        }

		let editData = null
        if (to.name == 'topic_edit') {
            let ret = await api.topicGet(to.params.id)
            if (ret.code) {
                $.message_error('抱歉，发生了错误')
                return next('/')
            }
            editData = ret.data
        }
        next(vm => {
            if (editData) {
                let date = new Date();
                date.setTime(editData.time * 1000)
                vm.topicInfo = editData
                vm.date = date
            }
        })
    },
    components: {
        markdownEditor
    }
}
</script>
