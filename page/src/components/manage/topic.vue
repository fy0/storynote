<template>
<div>
    <div style="margin-top: 15px;" v-if="noteText">{{noteText}}</div>
    <el-card v-else class="box-card" v-for="i in data_lst.items" :key="i.id">
        <div>
            <h3 class="topic-title">{{i.title}}</h3>
            <span v-if="i.id == state.data.user.id">[当前用户]</span>
        </div>
        <div>
            <span>权限：</span>
            <span v-for="v,k in state.data.misc.TOPIC_STATE">
                <span class="level-btn" v-if="k == i.state">{{v}}</span>
                <a class="level-btn" v-else href="javascript:void(0)" @click="stateChange(i, k)">{{v}}</a>
            </span>
        </div>
    </el-card>
</div>
</template>

<style scoped>
.level-btn {
    margin-right: 5px;
}

.box-card {
    margin-top: 10px;
}

.topic-title {    
    margin: 0;
    font-size: 2em;
}
</style>

<script>
import api from "../../netapi.js"
import state from "../../state.js"

export default {
    data () {
        return {
            state,
            data_lst: {},
            curitem: null,
            new_password: '',
            noteText: '加载中 ...',
            passwordResetDialogVisible: false,
        }
    },
    mounted: async function () {
        let ret = await api.manageTopicList();
        this.$set(this, "data_lst", ret.data);
        this.noteText = '';
    },
    methods: {
        showPasswordReset: function (item) {
            this.curitem = item;
            this.passwordResetDialogVisible = true;
        },
        stateChange: async function (item, state) {
            let ret = await api.manageUserChangeState(item.id, state);
            if (ret.code == 0) {
                item.state = state;
                $.message_success('操作成功！');
            } else $.message_error(api.retinfo[ret.code]);
        },
    },
}
</script>
