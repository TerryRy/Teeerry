const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
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
