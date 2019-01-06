export default {
    plugins: [
        '@uvue/core/plugins/asyncData',
        [
            '@uvue/core/plugins/vuex',
            {
                onHttpRequest: true
            }
        ],
        '@uvue/core/plugins/middlewares',
        '@uvue/core/plugins/errorHandler'
    ]
    // imports: [
    //     {
    //         src: 'element-ui',
    //         ssr: false
    //     }
    // ]
}
