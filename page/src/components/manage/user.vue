<template>
<div>
    <el-input class="search-box" placeholder="搜索 用户名/uid" icon="search" v-model="keyword" :on-icon-click="searchIconClick"></el-input>
    <el-card class="box-card" v-for="i in user_lst.items">
        <span>{{i.username}}</span>
        <div>
            <span>权限：</span>
            <a href="javascript:void(0)" @click="stateChange(i.id, 'del')">删除</a>
            <a href="javascript:void(0)" @click="stateChange(i.id, 'ban')">封禁</a>
            <a href="javascript:void(0)" @click="stateChange(i.id, 'normal')">正常</a>
            <a href="javascript:void(0)" @click="stateChange(i.id, 'writer')">作者</a>
            <a href="javascript:void(0)" @click="stateChange(i.id, 'writer')">管理</a>
        </div>
        <div>
            <a href="javascript:void(0)" @click="passwordReset(i.id)">密码重置</a>
            <a href="javascript:void(0)" @click="sessionReset(i.id)">会话重置</a>
        </div>
    </el-card>
</div>
</template>

<style>
</style>

<script>
import api from "../../netapi.js"

export default {
    data () {
        return {
            keyword: '',
            user_lst: {},
        }
    },
    mounted: async function () {
        let ret = await api.manageUserList();
        console.log(111, ret);
        this.$set(this, "user_lst", ret.data);
    },
    methods: {
        stateChange: async function (uid, level) {
            let funcMap = {
                'del': api.manageUserChangeLevelDel,
                'ban': api.manageUserChangeLevelBan,
                'normal': api.manageUserChangeLevelNormal,
                'writer': api.manageUserChangeLevelWriter,
                'admin': api.manageUserChangeLevelAdmin,
            }
            let func = funcMap[level];
            let ret = await func(uid);
            if (ret.code == 0) $.message_success('操作成功！');
            else $.message_error(api.retinfo[ret.code]);
        },
        passwordReset (uid) {
            ;
        },
        sessionReset (uid) {
            ;
        },
        searchIconClick () {
            ;
        }
    }
}
</script>
