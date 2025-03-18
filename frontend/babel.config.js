module.exports = {
  presets: ['@vue/cli-plugin-babel/preset'],
  plugins: [
    [
      'component',
      {
        libraryName: 'element-ui',
        styleLibraryName: 'theme-chalk',
        style: true
      }
    ],
    // 生产环境移除 console
    ['transform-remove-console', { exclude: ['error', 'warn'] }]
  ]
}
