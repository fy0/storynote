<template>
<div class="">
    <h3>注册</h3>
    <el-form :model="form" ref="form" label-width="60px" :rules="form_rules" style="width:50%;margin-left:-15px">
        <el-form-item label="账号" prop="username">
            <el-input type="text" v-model.trim="form.username" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="form.password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="重复" prop="password_again">
            <el-input type="password" v-model="form.password_again" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button :disabled="loading" type="primary" @click="submitForm('form')">提交</el-button>
            <el-button :disabled="loading" @click="resetForm('form')">重置</el-button>
        </el-form-item>
    </el-form>
</div>
</template>

<script>
import Vue from 'vue'
import api from "../../netapi.js"
import state from "../../state.js"
import nprogress from 'nprogress/nprogress.js'

export default {
    data () {
        return {
            form: {
                username: '',
                password: '',
                password_again: '',
            },
            loading: false,
            form_rules: {
                username: [
                    { required: true, message: '必须输入账号', trigger: 'blur' },
                    {
                        min: state.data.misc.USERNAME_REG_MIN, max: state.data.misc.USERNAME_REG_MAX, 
                        message: `账号长度应 ${state.data.misc.USERNAME_REG_MIN} 到 ${state.data.misc.USERNAME_REG_MAX} 之间`,
                        trigger: 'blur' 
                    }
                ],
                password: [
                    { required: true, message: '必须输入密码', trigger: 'blur' },
                    {
                        min: state.data.misc.PASSWORD_REG_MIN, max: state.data.misc.PASSWORD_REG_MAX,
                        message: `密码长度必须在 ${state.data.misc.PASSWORD_REG_MIN} 到 ${state.data.misc.PASSWORD_REG_MAX} 之间`, 
                        trigger: 'blur' 
                    }
                ],
                password_again: [
                    {
                        validator: (rule, value, callback) => {
                            if (value === '') {
                                callback(new Error('请再次输入密码'));
                            } else if (value !== this.form.password) {
                                callback(new Error('两次输入密码不一致!'));
                            } else {
                                callback();
                            }
                        },
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    methods: {
        resetForm (formName) {
            this.$refs[formName].resetFields();
        },
        setLoading (val) {
            this.loading = val;
            if (val) nprogress.start();
            else nprogress.done();
        },
        submitForm (formName) {
            this.$refs[formName].validate(async (valid) => {
                if (valid) {
                    this.setLoading(true);
                    let ret = await api.userSignup(this.form.username, this.form.password);
                    if (ret.code == 0) {
                        ret = await api.userInfo();                        
                        Vue.set(state.data, 'user', ret.data);
                        if (ret.code == 0) {
                            Vue.set(state.data, 'user', ret.data);
                            $.message_success(`注册成功！现以新的身份跳转首页。`);
                        } else {
                            $.message_error(`错误：${api.retinfo[ret.code]}`);
                        }
                        this.$router.replace({ path: '/'})
                    } else {
                        for (let i of ret.error_msgs) {
                            $.message_error(i);
                        }
                    }
                    this.setLoading(false);
                } else {
                    return false;
                }
            });
        },
    },
}
</script>

<style>

</style>
