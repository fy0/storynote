<template>
<div>
    <el-input class="search-box" placeholder="搜索 用户名/uid" icon="search" v-model="keyword" :on-icon-click="searchIconClick"></el-input>
    <el-card class="box-card" v-for="i in user_lst.items" :key="i.id">
        <div>
            <span>{{i.username}}</span>
            <span v-if="i.id == state.data.user.id">[当前用户]</span>
        </div>
        <div>
            <span>权限：</span>
            <span v-for="v,k in state.data.misc.USER_LEVEL">
                <span class="level-btn" v-if="k == i.level">{{v}}</span>
                <a class="level-btn" v-else href="javascript:void(0)" @click="stateChange(i, k)">{{v}}</a>
            </span>
        </div>
        <div>
            <a href="javascript:void(0)" @click="passwordResetDialogVisible = true">密码重置</a>
            <a href="javascript:void(0)" @click="sessionReset(i)">会话重置</a>
        </div>
    </el-card>
    <el-dialog title="密码重置" :visible.sync="passwordResetDialogVisible">

    </el-dialog>
</div>
</template>

<style scoped>
.level-btn {
    margin-right: 5px;
}
</style>

<script>
import api from "../../netapi.js"
import state from "../../state.js"

export default {
    data () {
        return {
            state,
            keyword: '',
            user_lst: {},
            passwordResetDialogVisible: false,
        }
    },
    mounted: async function () {
        let ret = await api.manageUserList();
        this.$set(this, "user_lst", ret.data);
    },
    methods: {
        stateChange: async function (item, level) {
            let ret = await api.manageUserChangeLevel(item.id, level);
            if (ret.code == 0) {
                item.level = level;
                $.message_success('操作成功！');
            } else $.message_error(api.retinfo[ret.code]);
        },
        passwordReset: async function (item, new_password) {
            let ret = await api.manageUserPasswordReset(item.id);
            if (ret.code == 0) {
                $.message_success('操作成功！');
            } else $.message_error(api.retinfo[ret.code]);
        },
        sessionReset: async function (item) {
            let ret = await api.manageUserKeyReset(item.id);
            if (ret.code == 0) {
                $.message_success('操作成功！');
            } else $.message_error(api.retinfo[ret.code]);
        },
        searchIconClick () {
            ;
        }
    }
}
</script>
