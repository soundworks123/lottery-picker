const { defineConfig } = require('@vue/cli-service')
const CompressionPlugin = require('compression-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')
const ImageMinimizerPlugin = require('image-minimizer-webpack-plugin')

module.exports = defineConfig({
  transpileDependencies: true,
  productionSourceMap: false,

  chainWebpack: config => {
    // 图片优化配置
    config.module
      .rule('images')
      .test(/\.(png|jpe?g|gif|svg)(\?.*)?$/)
      .use('image-webpack-loader')
      .loader('image-webpack-loader')
      .options({
        mozjpeg: { quality: 65 },
        optipng: { enabled: false },
        pngquant: { quality: [0.65, 0.9], speed: 4 },
        gifsicle: { interlaced: false }
      })
      .end()

    // 生产环境配置
    if (process.env.NODE_ENV === 'production') {
      // 启用 gzip 压缩
      config.plugin('compression').use(CompressionPlugin, [{
        test: /\.(js|css|html|svg)$/,
        threshold: 10240,
        deleteOriginalAssets: false
      }])

      // 优化 chunk 分割
      config.optimization.splitChunks({
        chunks: 'all',
        minSize: 20000,
        maxSize: 244000,
        cacheGroups: {
          elementUI: {
            name: 'chunk-elementUI',
            priority: 20,
            test: /[\\/]node_modules[\\/]element-ui[\\/]/
          },
          commons: {
            name: 'chunk-commons',
            minChunks: 2,
            priority: 10,
            reuseExistingChunk: true
          }
        }
      })

      // 压缩配置
      config.optimization.minimizer('terser').use(TerserPlugin, [{
        terserOptions: {
          compress: {
            drop_console: true,
            drop_debugger: true
          }
        }
      }])

      // 图片压缩
      config.optimization.minimizer('imageminimizer').use(ImageMinimizerPlugin, [{
        minimizer: {
          implementation: ImageMinimizerPlugin.imageminMinify,
          options: {
            plugins: [
              ['gifsicle', { interlaced: true }],
              ['jpegtran', { progressive: true }],
              ['optipng', { optimizationLevel: 5 }]
            ]
          }
        }
      }])
    }
  },

  // 开发服务器配置
  devServer: {
    hot: true,
    client: {
      overlay: {
        warnings: false,
        errors: true
      }
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
