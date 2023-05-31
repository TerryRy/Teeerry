const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
    proxy: {
      '/api': { // 请求的代称，写在Axios里的BaseUrl
        target: 'http://localhost:8000', // 真实请求URl
        // target: 'http://host.docker.internal:8000',
        //target: 'http://tc-back:8000',
        ws: true,
        changeOrigin: true, // 允许跨域
        pathRewrite:{
          '/api':''
        }
      }
    }
  },

  transpileDependencies: true,
  configureWebpack:{
    resolve:{
      alias:{
        'images':'@/assets/images',
        'common':'@/components/common',
        'homepage':'@/views/homepage',
        'login':'@/views/railway_admin/login',
        'train_add':'@/views/railway_admin/train_add',
        'train_change':'@/views/railway_admin/train_change',
        'workspace':'@/views/railway_admin/workspace',
        'reform_close_page':'@/views/reform_close_page',
        'welcome_page':'@/views/welcome_page'
      }
    }
  }
})
