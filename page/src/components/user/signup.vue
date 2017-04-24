<template>
<div class="">
    <h3>注册</h3>

    <el-form :model="form" :label-position="left" ref="form" label-width="40px" style="width:50%">
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
            <el-button type="primary" @click="submitForm('form')">提交</el-button>
            <el-button @click="resetForm('form')">重置</el-button>
        </el-form-item>
    </el-form>
</div>
</template>

<script>
import Vue from 'vue'
import api from "../../netapi.js"
import state from "../../state.js"

export default {
    data () {
        return {
            form: {
                username: '',
                password: '',
                password_again: '',
            },
        }
    },
    methods: {
        resetForm (formName) {
            this.$refs[formName].resetFields();
        },
        submitForm (formName) {
            this.$refs[formName].validate(async (valid) => {
                if (valid) {
                    let ret = await api.userSignup(this.form.username, this.form.password);
                    if (ret.code == 0) {
                        $.message_success(`注册成功！现以新的身份跳转首页。`);
                        this.$router.replace({ path: '/'})
                    } else {
                        for (let i of ret.error_msgs) {
                            $.message_error(i);
                        }
                    }
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
