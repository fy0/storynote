<template>
<div class="">
    <div class="edit-page-title">
        <h3 class="" v-if="!is_edit">新建主题</h3>
        <h3 class="" v-else>编辑主题</h3>
        <el-button class="right-top-btn" type="primary" :loading="loading" @click="send">{{postButtonText}}</el-button>
    </div>

    <form id="form_topic" method="POST" @submit.prevent="send">
        <div class="form-item">
            <el-input name="title" v-model="topicInfo.title" placeholder="这里填写标题，最长50个字" style="width: 70%; font-size: 15px; margin-right: 2%;"></el-input>
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
            <el-input name="link_to" v-model="topicInfo.link_to" placeholder="填写外站引用链地址(可选)" style="width: 70%; font-size: 15px; margin-right: 2%;"></el-input>
            <el-select v-model="topicInfo.state" placeholder="请选择" style="width: 27%; font-size: 15px; font-weight: bolder;">
                <el-option v-for="[v, k] in topicStateOptions" :key="parseInt(v)" :label="`状态：${k}`" :value="parseInt(v)"></el-option>
            </el-select>
        </div>
        <div class="form-item">
            <markdown-editor class="editor" ref="editor" v-model="topicInfo.content" rows="15" autofocus />
        </div>
        <div class="form-item">
            <el-button style="float: right" type="primary" :loading="loading" @click="send">{{postButtonText}}</el-button>
        </div>
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
    /* background-color: #fff; */
    /* color: #1f2d3d; */
}
</style>

<script>
import api from '../netapi.js'
import config from '../config.js'
import markdownEditor from '@/components/utils/markdown-editor.vue'
import './utils/topic-edit-fa.js'
import Objectid from 'objectid-js'

export default {
    data () {
        return {
            loading: false,
            date: new Date(),

            topicInfo: {
                title: '',
                link_to: '',
                board: null,
                content: ''
            },

            pickerOptions: {
                shortcuts: [{
                    text: '当前',
                    onClick (picker) {
                        picker.$emit('pick', new Date())
                    }
                }, {
                    text: '昨天',
                    onClick (picker) {
                        const date = new Date()
                        date.setTime(date.getTime() - 3600 * 1000 * 24)
                        picker.$emit('pick', date)
                    }
                }, {
                    text: '一周前',
                    onClick (picker) {
                        const date = new Date()
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
                        picker.$emit('pick', date)
                    }
                }]
            },

            token: ''
        }
    },
    computed: {
        topicStateOptions: function () {
            return Object.entries(this.$store.state.misc.TOPIC_STATE_TXT)
        },
        is_edit () {
            return this.$route.name === 'topic_edit'
        },
        postButtonText: function () {
            return this.loading ? '请等待'
                : (this.is_edit ? '编辑' : '发布')
        }
    },
    methods: {
        send: async function (e) {
            if (!this.topicInfo.title) {
                $.message_error('请输入一个标题！')
                return false
            }

            if (this.topicInfo.title.length < this.$store.state.misc.TITLE_LENGTH_MIN) {
                $.message_error(`标题应不少于 ${this.$store.state.misc.TITLE_LENGTH_MIN} 个字！`)
                return false
            }

            if (this.topicInfo.title.length > this.$store.state.misc.TITLE_LENGTH_MAX) {
                $.message_error(`标题应不多于 ${this.$store.state.misc.TITLE_LENGTH_MAX} 个字！`)
                return false
            }

            this.topicInfo.time = parseInt(this.date.getTime() / 1000)

            // 允许页面内容为空
            // if (!content) return;

            let ret
            let successText
            let failedText

            this.loading = true
            if (this.is_edit) {
                ret = await api.topicEdit(this.$route.params.id, this.topicInfo)
                successText = '编辑成功！已自动跳转至文章页面。'
                failedText = ret.msg || '编辑失败！'
            } else {
                ret = await api.topicNew(this.topicInfo)
                successText = '发表成功！已自动跳转至文章页面。'
                failedText = ret.msg || '编辑失败！'
            }

            if (ret.code === 0) {
                localStorage.setItem('topic-post-cache-clear', 1)
                this.$router.push({ name: 'topic', params: { id: ret.data.id } })
                $.message_success(successText)
            } else {
                $.message_error(failedText)
                // 注意：发布成功会跳转，故不做复位，失败则复位
                this.loading = false
            }
        }
    },
    created: async function () {
        if (!this.$store.state.user) {
            $.message_error('抱歉，无权访问此页面')
            return this.$router.replace('/')
        }

        let editData = null
        if (this.$route.name === 'topic_edit') {
            let ret = await api.topicGet(this.$route.params.id)
            if (ret.code) {
                $.message_error('抱歉，发生了错误')
                return this.$router.replace('/')
            }
            editData = ret.data
        }

        if (editData) {
            let date = new Date()
            date.setTime(editData.time * 1000)
            this.topicInfo = editData
            this.date = date
        }

        if (localStorage.getItem('topic-post-cache-clear')) {
            // 我不知道为什么，在地址跳转前进行 storage 的清除工作，
            // 并不会实质上起效，因此这是一个替代手段，效果比较理想。
            localStorage.removeItem('topic-post-title')
            localStorage.removeItem('smde_topic-post-content')
            localStorage.removeItem('topic-post-cache-clear')
        }

        if (!this.is_edit) {
            this.title = localStorage.getItem('topic-post-title') || ''
        }

        let uploadImage = async function (editor, fileList) {
            let theFile = null
            if (fileList.length === 0) return

            for (let i of fileList) {
                if (i.type.indexOf('image') !== -1) {
                    theFile = i
                    break
                }
            }
            if (!theFile) return false

            let placeholder = `![Uploading ${theFile['name']} - ${(new Objectid()).toString()} ...]()`
            editor.replaceRange(placeholder, {
                line: editor.getCursor().line,
                ch: editor.getCursor().ch
            })

            let ret = await api.qnUpload(theFile)
            if (ret.key) {
                let url = `${config.qiniu.host}/${ret.key}-${config.qiniu.suffix}`
                let newTxt = `![](${url})`
                let offset = newTxt.length - placeholder.length
                let cur = editor.getCursor()
                editor.setValue(editor.getValue().replace(placeholder, newTxt + '\n'))
                editor.setCursor(cur.line, cur.ch + offset)
            }
        }

        this.$nextTick(() => {
            let editor = this.$refs.editor
            let cm = editor.simplemde.codemirror
            cm.on('drop', async (editor, e) => {
                await uploadImage(editor, e.dataTransfer.files)
            })
            cm.on('paste', async (editor, e) => {
                await uploadImage(editor, e.clipboardData.files)
                return false
            })
        })
    },
    watch: {
        title: _.debounce(function (val, oldVal) {
            localStorage.setItem('topic-post-title', val)
        }, 5000)
    },
    components: {
        markdownEditor
    }
}
</script>
