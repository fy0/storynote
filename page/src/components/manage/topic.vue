<template>
<div>
    <div style="margin-top: 15px;" v-if="noteText">{{noteText}}</div>
    <el-card v-else class="box-card" v-for="i in data_lst.items" :key="i.id">
        <div>
            <div>
                <h3 class="topic-title">{{i.title}}</h3>
                <nuxt-link :to="{ name: 'topic_edit', params: {id: i.id}}">编辑</nuxt-link>
            </div>
            <span>作者： <b>{{i.user.username}}</b>
                <span v-if="i.user.id === $store.state.user.id">[当前用户]</span>
            </span>
        </div>
        <div>
            <span>权限：</span>
            <span v-for="(v, k) in $store.state.misc.TOPIC_STATE_TXT" :key="k">
                <span class="level-btn" v-if="k === i.state">{{v}}</span>
                <a class="level-btn" v-else href="javascript:void(0)" @click="stateChange(i, k)">{{v}}</a>
            </span>
        </div>
    </el-card>

    <span v-if="data_lst.last_page === data_lst.first_page">
        <span v-if="data_lst && data_lst.prev_page">
            <a href="javascript:void(0)" @click="loadData(data_lst.prev_page)">上一页</a>
        </span>
        <span v-if="data_lst && data_lst.next_page">
            <a href="javascript:void(0)" @click="loadData(data_lst.next_page)">下一页</a>
        </span>
    </span>
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
    display: inline;
}
</style>

<script>
import api from '../../netapi.js'

export default {
    data () {
        return {
            data_lst: {},
            new_password: '',
            noteText: '加载中 ...',
            passwordResetDialogVisible: false
        }
    },
    mounted: async function () {
        let ret = await api.manageTopicList()
        this.$set(this, 'data_lst', ret.data)
        this.noteText = ''
    },
    methods: {
        loadData: async function (page) {
            let ret = await api.manageTopicList(page)
            this.$set(this, 'data_lst', ret.data)
            this.noteText = ''
        },
        stateChange: async function (item, state) {
            let ret = await api.manageUserChangeState(item.id, state)
            if (ret.code === 0) {
                item.state = state
                $.message_success('操作成功！')
            } else $.message_error(api.retinfo[ret.code])
        }
    }
}
</script>
