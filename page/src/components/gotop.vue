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
    color: #056ef0;
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
        let updatePosition = function () {
            console.log(111, this.y)
        }
        // state.data.iscroll.on('scroll', updatePosition);
        // state.data.iscroll.on('scrollEnd', updatePosition);
        // $.message('warning', '123');
        // $.message('success', '操作已完成');

        var timer = setInterval(() => {
            this.showGoTop = document.body.scrollTop > 1;
        }, 100);
    },
    methods: {
        gotop: function () {
            // state.data.iscroll.refresh ('#app', 0, 0);

            var top = document.body.scrollTop;
            var timer = setInterval(() => {
                top -= Math.abs(top * 0.1);
                if (top <= 1) {
                    top = 0;
                    clearInterval(timer);
                }
                document.body.scrollTop = top;
            }, 20);

            //state.data.iscroll.scrollToElement(document.querySelector('.page-header'));
        }
    }
}
</script>

<style>

</style>
