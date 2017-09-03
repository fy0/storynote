<template>
<div class="topic-content entry">
    <div class="content" v-if="topic">
        <h1 class="post-title"><router-link :to="{ path: '/t/' + topic.id }">{{topic.title}}</router-link></h1>
        
        <div class="post-info">
            <span>{{topic.user.name}}</span>
            <span>{{getTime(topic.time)}}</span>
            <router-link v-if="canEdit" :to="{ name: 'topic_edit', params: {id: topic.id}}">编辑</router-link>    
        </div>

        <div v-html="marked(topic.content)"></div>

        <div class="tags">
            <el-tag v-for="tag in topic_tags" :key="tag" :closable="canEdit" :close-transition="true" @close="handleClose(tag)">
                <!-- 这里真是坑 -->
                <router-link :to="{ name: 'tag', params: {name: tag.tag.name}}">{{tag.tag.name}}</router-link>
            </el-tag>

            <span v-if="canEdit">
                <el-input
                    class="tag-new-container"
                    v-if="inputVisible"
                    v-model="inputValue"
                    ref="saveTagInput"
                    icon="circle-close"
                    size="mini"
                    :on-icon-click="tagInputClose"
                    @keyup.enter.native="handleInputConfirm"
                >
                </el-input>
                <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
            </span>
        </div>

        <div class="comment-info">
            <span class="comment-info-title">{{comments_length}} 条评论</span>
            <span class="comment-info-line"></span>
        </div>

        <div class="comment" v-for="(i, index) in comments" :key="index">
            <div class="ic-comment-body">
                <div class="ic-comment-content" v-html="marked(i.content)"></div>
                <div class="ic-comment-meta">
                    <b>{{i.user.name}}</b>
                    <time>{{time_to_text(i.time)}}</time>
                    <span> | </span>
                    <span>#{{i.id}}</span>
                </div>
            </div>
            <div class="divider-line" v-if="index != comments.length-1"></div>
        </div>

        <div v-if="comments_page > 1">
            <span v-for="index in comments_page" :key="index">
                <span class="comment-page-btn" v-if="$route.params.cmtpage == index">{{index}}</span>
                <router-link class="comment-page-btn" v-else :to="{ name: 'topic', params: {id: topic.id, cmtpage: index}}" replace>{{index}}</router-link>
            </span>
        </div>

        <div v-if="state.data.user" style="margin-top: 20px">
            <form method="POST">
                <div>
                    <textarea name="content" rows="5" placeholder="" style="width:100%;border-color:#d9d9d9" v-model="user_comment_text"></textarea>
                </div>
                <div>
                    <el-button @click="commentPost">发表</el-button>
                    <span style="margin-left:10px" id="reply_msg"></span>
                </div>
            </form>
        </div>
        <div style="padding: 20px" v-else>
            需要 <router-link :to="{ path: `/signin` }">登录</router-link> 后方可回复, 如果你还没有账号你可以 <router-link :to="{ path: `/signup` }">注册</router-link> 一个帐号。
        </div>
 
    </div>
    <loading v-else></loading>
</div>
</template>

<style scoped>
.tags {
    margin-bottom: 20px;
}

.tags > div {
    margin-right: 5px;
}

.el-tag > a {
    color: #fff;
}

.post-title {
    word-wrap: break-word;
    margin: 0.3em 0 0;
}

.post-title > a {
    color: #000;
}

.post-info {
    color: rgb(153, 153, 153);
    padding: 0px;
    font-size: small;
}
</style>

<script>
import marked from 'marked'
import api from "../netapi.js"
import state from "../state.js"
import Loading from "./utils/loading.vue"

export default {
    data () {
        return {
            state,
            topic: null,
            comments: [], // 当前显示的评论数
            comments_length: '?', // 总评论数
            comments_page: 1,
            user_comment_text: '',
            time_to_text: $.time_to_text,
            topic_tags: [],
            inputVisible: false,
            inputValue: ''
        }
    },
    computed: {
        canEdit: function () {
            if (!state.data.user) return;
            return (state.data.user.level == 100) || (state.data.user.id == this.topic.user.id);
        }
    },
    methods: {
        marked,
        getTime: (timestamp) => {
            return $.get_time(timestamp);
        },

        handleClose: async function (tag) {
            let ret = await api.tagRemoveFromPostById(tag.id);
            this.topic_tags.splice(this.topic_tags.indexOf(tag), 1);
        },

        showInput: function () {
            this.inputVisible = true;
            this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },

        tagInputClose: function () {
            this.inputValue = '';
            this.inputVisible = false;
        },

        handleInputConfirm: async function () {
            let inputValue = this.inputValue;
            if (inputValue) {
                let ret = await api.tagAddToTopic(inputValue, this.topic.id, true);
                if (ret.code == api.retcode.SUCCESS) {
                    this.topic_tags.push(ret.data);
                } else {
                    $.message_error(api.retinfo[ret.code])
                }
            }
            this.inputVisible = false;
            this.inputValue = '';
        },
    
        commentFetch: async function (page=1) {
            let ret = await api.commentGet(this.topic.id, page);
            if (ret.code == 0) {
                this.comments_length = ret.data.count;
                this.comments = ret.data.items;
                this.comments_page = Math.ceil(this.comments_length / ret.data.page_size);
            }
        },
        commentPost: async function () {
            let ret = await api.commentPost(this.topic.id, this.user_comment_text);
            if (ret.code == 0) {
                this.user_comment_text = '';
                this.commentFetch(this.comments_page);
            }
        }
    },
    mounted: async function () {
    },
    watch: {
        '$route' (to, from) {
            if (to.params.cmtpage) {
                // this.commentFetch(to.params.cmtpage);
            }
        }
    },
    beforeRouteEnter: async (to, from, next) => {
        // 获取文章内容
        let topic = await api.topicGet(to.params.id);

        if (topic.code == api.retcode.SUCCESS) {
            // 获取评论
            let comment = await api.commentGet(topic.data.id, to.params.cmtpage || 1);

            if (comment.code == api.retcode.SUCCESS) {
                return next(vm => {
                    vm.topic = topic.data;
                    vm.topic_tags = topic.data.tags;

                    vm.comments_length = comment.data.count;
                    vm.comments = comment.data.items;
                    vm.comments_page = Math.ceil(vm.comments_length / comment.data.page_size);
                });
            }
        }

        $.message_error(`错误：${api.retinfo[ret.code]}`);
        return next('/');
    },
    components: {
        Loading,
    }
}
</script>


<style>
.tag-new-container {
    width: 150px;
}

.tag-new-container > input {
    min-height: 25px;
}
</style>

<style scoped>
.el-tag:not(:last-of-type) {
    margin-right: 5px;
}
</style>
