<template>
<div v-if="$store.state.user">
    <p>已经登录，身份为 {{$store.state.user.name}}</p>
    <nuxt-link :to="{ path: '/signout' }">注销</nuxt-link>
</div>
<div v-else>
    <h4>登录</h4>
    <el-form :model="form" ref="form" label-width="60px" :rules="form_rules" style="width:50%;margin-left:-15px">
        <el-form-item label="账号" prop="username">
            <el-input type="text" v-model.trim="form.username" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="form.password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="" prop="remember">
            <el-checkbox v-model="form.remember">30天内记住登录</el-checkbox>
        </el-form-item>
        <el-form-item >
            <el-button :disabled="loading" type="primary" @click="submitForm('form')">提交</el-button>
            <el-button :disabled="loading" @click="resetForm('form')">重置</el-button>
        </el-form-item>
    </el-form>
</div>
</template>

<script>
import api from '../../netapi.js'
// import nprogress from 'nprogress/nprogress.js'

export default {
    data () {
        return {
            loading: false,
            form: {
                username: '',
                password: '',
                remember: true
            },
            form_rules: {
                username: [
                    { required: true, message: '必须输入账号', trigger: 'blur' },
                    {
                        min: this.$store.state.misc.USERNAME_MIN,
                        max: this.$store.state.misc.USERNAME_MAX,
                        message: `用户名不合法`,
                        trigger: 'blur'
                    }
                ],
                password: [
                    { required: true, message: '必须输入密码', trigger: 'blur' },
                    {
                        min: this.$store.state.misc.PASSWORD_MIN,
                        max: this.$store.state.misc.PASSWORD_MAX,
                        message: `密码长度必须在 ${this.$store.state.misc.PASSWORD_MIN} 到 ${this.$store.state.misc.PASSWORD_MAX} 之间`,
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    head () {
        return {
            title: `登录`
        }
    },
    methods: {
        resetForm (formName) {
            this.$refs[formName].resetFields()
        },
        setLoading (val) {
            this.loading = val
            // if (val) nprogress.start()
            // else nprogress.done()
        },
        submitForm (formName) {
            this.$refs[formName].validate(async (valid) => {
                if (valid) {
                    this.setLoading(true)
                    let ret = await api.userSignin(this.form.username, this.form.password, this.form.remember)
                    if (ret.code === 0) {
                        ret = await api.userInfo()
                        if (ret.code === 0) {
                            this.$store.commit('SET_USERDATA', ret.data)
                            $.message_success(`欢迎回来，${ret.data.name}！`)
                        } else {
                            $.message_error(`错误：${api.retinfo[ret.code]}`)
                        }
                        this.$router.replace({ path: '/' })
                    } else {
                        for (let i of ret.error_msgs) {
                            $.message_error(i)
                        }
                    }
                    this.setLoading(false)
                } else {
                    return false
                }
            })
        }
    }
}
</script>

<style>

</style>
