<template>
    <div class="timer"></div>
</template>

<style>
/* Timer*/
.timer{
    width: 48px;
    height: 48px;
    background-color: transparent;
    box-shadow: inset 0px 0px 0px 2px rgba(170,170,170,1);
    border-radius: 50%;
    position: relative;
    margin-left: 31%;
    margin-right: auto;
    top: 20vh;
 }
.timer:after, .timer:before{
    position: absolute;
    content:"";
    background-color: rgba(170,170,170,1);
}
.timer:after{
    width: 20px;
    height: 2px;
    top: 22px;
    left: 22px;
    -webkit-transform-origin: 1px 1px;
       -moz-transform-origin: 1px 1px;
            transform-origin: 1px 1px;
    -webkit-animation: minhand 1s linear infinite;
       -moz-animation: minhand 1s linear infinite;
            animation: minhand 1s linear infinite;
}

.timer:before{
    width: 16px;
    height: 2px;
    top: 22px;
    left: 22px;
    -webkit-transform-origin: 1px 1px;
       -moz-transform-origin: 1px 1px;
            transform-origin: 1px 1px;
    -webkit-animation: hrhand 4s linear infinite;
       -moz-animation: hrhand 4s linear infinite;
            animation: hrhand 4s linear infinite;
}

@-webkit-keyframes minhand{
    0%{-webkit-transform:rotate(0deg)}
    100%{-webkit-transform:rotate(360deg)}
}
@-moz-keyframes minhand{
    0%{-moz-transform:rotate(0deg)}
    100%{-moz-transform:rotate(360deg)}
}
@keyframes minhand{
    0%{transform:rotate(0deg)}
    100%{transform:rotate(360deg)}
}

@-webkit-keyframes hrhand{
    0%{-webkit-transform:rotate(0deg)}
    100%{-webkit-transform:rotate(360deg)}
}
@-moz-keyframes hrhand{
    0%{-moz-transform:rotate(0deg)}
    100%{-moz-transform:rotate(360deg)}
}
@keyframes hrhand{
    0%{transform:rotate(0deg)}
    100%{transform:rotate(360deg)}
}
</style>

<script>
export default {
    data () {
        return {
        }
    }
}
</script>
