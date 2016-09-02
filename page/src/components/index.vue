<template>
<div>
    <div class="nav">
        <a href="#">标签</a>
        <a href="#">文章</a>
        <a href="#">项目</a>
    </div>
    <h1>这里是标题</h1>
    <div class="pure-g">
        <div class="pure-u-3-4">
            <div class="article-item" v-for="item in topics">
                <p><a>{{item.title}}</a></p>
                <p>{{item.date}}</p>
                <div class="divider-line"></div>
            </div>
        </div>
        <div class="pure-u-1-4">
            <img class="avatar" src="../assets/images/doge.png"/>
        </div>
    </div>
</div>
</template>

<script>
import api from "../netapi.js"

export default {
    data () {
        return {
            topics: [
                {title: '这是一篇文章1', author: 'fy', date: '2016-01-01', brief: '简介简介简介简介简介'},
                {title: '这是一篇文章2', author: 'fy', date: '2016-01-01', brief: '简介简介简介简介简介'},
                {title: '这是一篇文章3', author: 'fy', date: '2016-01-01', brief: '简介简介简介简介简介'},
            ],
            msg: 'Hello Vue 2.0!'
        }
    },
    mounted: function () {
        api.test();
        console.log(1111111);
    }
}
</script>

<style>
    .nav {
        float: right;
    }

    .article-item {
    }

    .divider-line {
        border-bottom: #EBF2F6 1px solid;
        width: 50%;
    }

    .avatar {
        float: left;
        width: 50px;
        height: 50px;
        min-height: 50px;
        border-bottom-width: 0px !important; /* fix for entry.css */
    }
</style>
