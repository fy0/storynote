<template>
<div>
    <form method="post" class="pure-form" @submit.prevent="send">
        <fieldset>
            <h3>登录</h3>
            <div class="ic-form-row">
                <label for="username">帐号:</label>
                <input type="text" name="username" id="username" value="">
            </div>
            <div class="ic-form-row">
                <label for="password">密码:</label>
                <input type="password" name="password" id="password" value="">
            </div>
            <div class="ic-form-row">
                <label><input name="remember" type="checkbox" checked> 记住密码</label>
            </div>

            <div class="ic-form-row">
                <input class="pure-button pure-button-primary" type="submit" value="登 录">
            </div>
        </fieldset>
    </form>
</div>
</template>

<script>
import api from "../netapi.js"

export default {
    data () {
        return {
            msg: 'Hello Vue 2.0!'
        }
    },
    methods: {
        send: async function (e) {
            let formdata = new FormData(e.target);
            let username = (formdata.get("username") || "").trim();
            let password = (formdata.get("password") || "").trim();
            let ret = await api.userSignin(username, password);
            if (ret.code == 0) {
                ret = await api.userInfo();
                if (ret.code == 0) {
                    Vue.set(state.data, 'user', ret.data);
                }
                this.$router.replace({ path: '/'})
            } else {
                console.log(ret);
                alert(ret.error_msgs);
            }
        }
    },
}
</script>

<style>

</style>
