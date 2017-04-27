<template>
<div class="topic-content entry">
    <div class="content" v-if="topic">
        <h1 class="post-title"><router-link :to="{ path: '/t/' + topic.id }">{{topic.title}}</router-link></h1>
        
        <div class="post-info">
            <span>{{topic.user.name}}</span>
            <span>{{getTime(topic.time)}}</span>
        </div>

        
        <div v-html="marked(topic.content)"></div>

        <div class="tags">
            <el-tag
                :key="tag"
                v-for="tag in dynamicTags"
                :closable="true"
                :close-transition="false"
                @close="handleClose(tag)"
            >
            {{tag}}
            </el-tag>
            <el-input
                class="input-new-tag"
                v-if="inputVisible"
                v-model="inputValue"
                ref="saveTagInput"
                size="mini"
                @keyup.enter.native="handleInputConfirm"
                @blur="handleInputConfirm"
            >
            </el-input>
            <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
        </div>

        <div class="comment-info">
            <span class="comment-info-title">{{comments_length}} 条评论</span>
            <span class="comment-info-line"></span>
        </div>

        <div class="comment" v-for="(i, index) in comments">
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
            <span v-for="index in comments_page">
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

<style>

.tags {
    margin-bottom: 20px;
}

.tags > div {
    margin-right: 5px;
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
            dynamicTags: ['标签一', '标签二', '标签三'],
            inputVisible: false,
            inputValue: ''
        }
    },
    methods: {
        marked,
        getTime: (timestamp) => {
            return $.get_time(timestamp);
        },
        handleClose(tag) {
            this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
        },

        showInput() {
            this.inputVisible = true;
            this.$nextTick(_ => {
                this.$refs.saveTagInput.$refs.input.focus();
            });
        },

        handleInputConfirm() {
            let inputValue = this.inputValue;
            if (inputValue) {
                this.dynamicTags.push(inputValue);
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
            console.log(ret);
        }
    },
    mounted: async function () {
        let ret = await api.topicGet(this.$route.params.id);
        if (ret.code == 0) {
            this.$set(this, "topic", ret.data);
            this.commentFetch(this.$route.params.cmtpage || 1);
        }
    },
    watch: {
        '$route' (to, from) {
            if (to.params.cmtpage) {
                this.commentFetch(to.params.cmtpage);
            }
        }
    },
    components: {
        Loading,
    }
}
</script>

<style>

</style>
