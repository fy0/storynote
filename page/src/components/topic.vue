<template>
<div class="topic-content entry">
    <div class="content" v-if="topic">
        <h1 class="post-title">{{topic.title}}</h1>
        <div class="post-info">
            <span>{{topic.user.name}}</span>
            <span>{{getTime(topic.time)}}</span>
        </div>
        <div v-html="marked(topic.content)"></div>

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
                    <span>#{{index+1}}</span>
                </div>
            </div>
            <div class="divider-line" v-if="index != comments.length-1"></div>
        </div>

        <div v-if="state.data.user" style="margin-top: 20px">
            <form method="POST">
                <div>
                    <textarea name="content" rows="5" placeholder="" style="width:100%;border-color:#d9d9d9" v-model="comment_text"></textarea>
                </div>
                <div>
                    <span class="pure-button" @click="commentPost">发表</span>
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
.post-title {
    word-wrap: break-word;
    margin: 0.3em 0 0;
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
import Loading from "./loading.vue"

export default {
    data () {
        return {
            state,
            topic: null,
            comments: [], // 当前显示的评论数
            comments_length: '?', // 总评论数
            comment_text: '',
            time_to_text: $.time_to_text,
        }
    },
    methods: {
        marked,
        getTime: (timestamp) => {
            return $.get_time(timestamp);
        },
        commentFetch: async function () {
            let ret = await api.commentGet(this.topic.id);
            if (ret.code == 0) {
                this.comments_length = ret.data.count;
                this.comments = ret.data.items;
            }
        },
        commentPost: async function () {
            let ret = await api.commentPost(this.topic.id, this.comment_text);
            if (ret.code == 0) {
                this.comment_text = '';
                this.commentFetch();
            }
            console.log(ret);
        }
    },
    mounted: async function () {
        let ret = await api.topicGet(this.$route.params.id);
        if (ret.code == 0) {
            this.$set(this, "topic", ret.data);
            this.commentFetch();
        }
    },
    components: {
        Loading,
    }
}
</script>

<style>

</style>
