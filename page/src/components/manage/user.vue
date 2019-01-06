<template>
<div>
    <el-input class="search-box" placeholder="搜索 用户名/uid" icon="search" v-model="keyword" :on-icon-click="searchIconClick"></el-input>
    <div style="margin-top: 15px;" v-if="noteText">{{noteText}}</div>
    <el-card v-else class="box-card" v-for="i in user_lst.items" :key="i.id">
        <div>
            <span>{{i.username}}</span>
            <span v-if="i.id === state.data.user.id">[当前用户]</span>
        </div>
        <div>
            <span>权限：</span>
            <span v-for="(v, k) in state.data.misc.USER_LEVEL_TXT" :key="k">
                <span class="level-btn" v-if="k === i.level">{{v}}</span>
                <a class="level-btn" v-else href="javascript:void(0)" @click="stateChange(i, k)">{{v}}</a>
            </span>
        </div>
        <div>
            <el-button type="danger" size="small" @click="showPasswordReset(i)">密码重置</el-button>
            <el-button type="primary" size="small" @click="sessionReset(i)">会话重置</el-button>
        </div>
    </el-card>
    <el-dialog title="密码重置" :visible.sync="passwordResetDialogVisible" :lock-scroll='false'>
        <el-form>
            <el-form-item label="新密码">
                <el-input type="text" v-model="new_password"></el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="passwordResetDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="passwordReset()">确 定</el-button>
        </span>
    </el-dialog>
</div>
</template>

<style scoped>
.level-btn {
    margin-right: 5px;
}

.box-card {
    margin-top: 10px;
}
</style>

<script>
import api from '../../netapi.js'
import state from '../../state.js'

export default {
    data () {
        return {
            state,
            keyword: '',
            user_lst: {},
            curitem: null,
            new_password: '',
            noteText: '加载中 ...',
            passwordResetDialogVisible: false
        }
    },
    mounted: async function () {
        let ret = await api.manageUserList()
        this.$set(this, 'user_lst', ret.data)
        this.noteText = ''
    },
    methods: {
        showPasswordReset: function (item) {
            this.curitem = item
            this.passwordResetDialogVisible = true
        },
        stateChange: async function (item, level) {
            let ret = await api.manageUserChangeLevel(item.id, level)
            if (ret.code === 0) {
                item.level = level
                $.message_success('操作成功！')
            } else $.message_error(api.retinfo[ret.code])
        },
        passwordReset: async function () {
            let ret = await api.manageUserPasswordReset(this.curitem.id, this.new_password)
            if (ret.code === 0) {
                $.message_success('操作成功！')
            } else $.message_error(api.retinfo[ret.code])
            this.passwordResetDialogVisible = false
        },
        sessionReset: async function (item) {
            this.$confirm('确认重置？', { lockScroll: false }).then(async _ => {
                let ret = await api.manageUserKeyReset(item.id)
                if (ret.code === 0) {
                    $.message_success('操作成功！')
                } else $.message_error(api.retinfo[ret.code])
            }).catch(_ => {})
        },
        searchIconClick: async function () {
            this.noteText = '加载中 ...'
            let ret = await api.manageUserList(this.keyword)
            if (ret.code === 0) {
                this.$set(this, 'user_lst', ret.data)
                this.noteText = ret.data.items.length ? '' : '未找到数据'
            } else $.message_error(api.retinfo[ret.code])
            this.passwordResetDialogVisible = false
        }
    },
    watch: {
        'keyword': _.debounce(function (val, oldVal) {
            this.searchIconClick()
        }, 1000)
    }
}
</script>
