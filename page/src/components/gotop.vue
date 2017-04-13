<template>
<div class="gotop" @click="gotop" v-show="showGoTop">
    <i class="fa fa-arrow-up" aria-hidden="true"></i>
</div>
</template>

<style>
.gotop {
    position: fixed;
    right: 5%;
    bottom: 5%;
    height: 40px;
    width: 40px;
    color: #056ef0;
    text-align: center;
    line-height: 40px;
    cursor: pointer;
}

.tipbox > .item {
}
</style>

<script>
import state from "../state.js"

export default {
    data () {
        return {
            state,
            showGoTop: false,
        }
    },
    mounted: async function () {
        var timer = setInterval(() => {
            this.showGoTop = document.body.scrollTop > 1;
        }, 100);
    },
    methods: {
        gotop: function () {
            var top = document.body.scrollTop;
            var timer = setInterval(() => {
                top -= Math.abs(top * 0.1);
                if (top <= 1) {
                    top = 0;
                    clearInterval(timer);
                }
                document.body.scrollTop = top;
            }, 20);
        }
    }
}
</script>

<style>
</style>
