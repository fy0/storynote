<template>
<div class="">
    <form method="post" class="pure-form" @submit.prevent="send">
        <fieldset>
            <div class="pure-controls">
                <h3>注册</h3>
            </div>

            <div class="ic-form-row">
                <label for="username">帐号:</label>
                <input type="text" name="username" id="username" value="">
            </div>
            <div class="ic-form-row">
                <label for="password">密码:</label>
                <input type="password" name="password" id="password" value="">
            </div>
            <div class="ic-form-row">
                <label for="password_again">重复:</label>
                <input type="password" name="password_again" id="password_again" value="">
            </div>

           <div class="ic-form-row">
                <input class="pure-button pure-button-primary" type="submit" name="" value="注 册">
            </div>
        </fieldset>
    </form>
</div>
</template>

<script>
export default {
    data () {
        return {
            msg: 'Hello Vue 2.0!'
        }
    }
}
</script>

<style>

</style>
