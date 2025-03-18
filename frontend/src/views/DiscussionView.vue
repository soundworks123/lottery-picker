/* eslint-disable */
/* eslint-disable prettier/prettier */
<template>
  <div class="discussion">
    <el-card class="discussion-card">
      <div slot="header">
        <h2>讨论区</h2>
        <el-button type="primary" @click="showPostDialog">发布新帖</el-button>
      </div>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-select v-model="filter.category" placeholder="选择分类">
              <el-option label="全部" value=""></el-option>
              <el-option label="选号经验" value="experience"></el-option>
              <el-option label="中奖分享" value="winning"></el-option>
              <el-option label="技术讨论" value="technical"></el-option>
              <el-option label="其他" value="other"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filter.sort" placeholder="排序方式">
              <el-option label="最新发布" value="newest"></el-option>
              <el-option label="最多评论" value="most_comments"></el-option>
              <el-option label="最多点赞" value="most_likes"></el-option>
            </el-select>
          </el-col>
          <el-col :span="12">
            <el-input
              v-model="filter.search"
              placeholder="搜索帖子"
              prefix-icon="el-icon-search"
            >
            </el-input>
          </el-col>
        </el-row>
      </div>

      <!-- 帖子列表 -->
      <div class="post-list">
        <el-card v-for="post in posts" :key="post.id" class="post-card">
          <div class="post-header">
            <div class="post-title">
              <h3 @click="showPostDetail(post)">{{ post.title }}</h3>
              <el-tag size="small" :type="getCategoryType(post.category)">
                {{ getCategoryLabel(post.category) }}
              </el-tag>
            </div>
            <div class="post-meta">
              <span>作者: {{ post.author }}</span>
              <span>发布时间: {{ formatDate(post.createTime) }}</span>
              <span>
                <i class="el-icon-view"></i>
                {{ post.views }}
              </span>
              <span>
                <i class="el-icon-chat-dot-round"></i>
                {{ post.comments }}
              </span>
              <span>
                <i class="el-icon-star-on"></i>
                {{ post.likes }}
              </span>
            </div>
          </div>
          <div class="post-content">
            <p>{{ post.summary }}</p>
          </div>
          <div class="post-footer">
            <el-button type="text" @click="showPostDetail(post)">查看详情</el-button>
            <el-button type="text" @click="handleLike(post)">
              <i :class="post.isLiked ? 'el-icon-star-on' : 'el-icon-star-off'"></i>
              点赞
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          @current-change="handlePageChange"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
        >
        </el-pagination>
      </div>
    </el-card>

    <!-- 发帖对话框 -->
    <el-dialog 
      title="发布新帖" 
      :visible.sync="postDialogVisible" 
      width="60%" 
      :close-on-click-modal="false"
      :destroy-on-close="true"
    >
      <el-form 
        :model="newPost" 
        :rules="postRules"
        ref="postForm"
        label-width="80px" 
        class="post-form"
      >
        <el-form-item label="标题" prop="title">
          <el-input 
            v-model="newPost.title" 
            placeholder="请输入标题"
            maxlength="100"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select 
            v-model="newPost.category" 
            placeholder="请选择分类"
            style="width: 100%"
          >
            <el-option label="选号经验" value="experience"></el-option>
            <el-option label="中奖分享" value="winning"></el-option>
            <el-option label="技术讨论" value="technical"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            type="textarea"
            v-model="newPost.content"
            :rows="10"
            placeholder="请输入内容"
            maxlength="2000"
            show-word-limit
          >
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="postDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitPost">发布</el-button>
      </div>
    </el-dialog>

    <!-- 帖子详情对话框 -->
    <el-dialog
      :title="currentPost.title"
      :visible.sync="detailDialogVisible"
      width="70%"
    >
      <div class="post-detail">
        <div class="post-info">
          <span>作者: {{ currentPost.author }}</span>
          <span>发布时间: {{ formatDate(currentPost.createTime) }}</span>
          <span>
            <i class="el-icon-view"></i>
            {{ currentPost.views }}
          </span>
          <span>
            <i class="el-icon-chat-dot-round"></i>
            {{ currentPost.comments }}
          </span>
          <span>
            <i class="el-icon-star-on"></i>
            {{ currentPost.likes }}
          </span>
        </div>
        <div class="post-content">
          {{ currentPost.content }}
        </div>
        <div class="comments-section">
          <h4>评论 ({{ currentPost.comments }})</h4>
          <div class="comment-list">
            <div
              v-for="comment in currentPost.commentList"
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-header">
                <span class="comment-author">{{ comment.author }}</span>
                <span class="comment-time">{{ formatDate(comment.createTime) }}</span>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
          <div class="comment-form">
            <el-input
              type="textarea"
              v-model="newComment"
              :rows="3"
              placeholder="写下你的评论..."
              maxlength="500"
              show-word-limit
              resize="none"
            >
            </el-input>
            <div class="comment-form-footer">
              <el-button type="primary" @click="submitComment" :disabled="!newComment.trim()">
                发表评论
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'DiscussionView',
  data() {
    return {
      filter: {
        category: '',
        sort: 'newest',
        search: '',
      },
      posts: [
        {
          id: 1,
          title: '分享我的双色球选号经验',
          category: 'experience',
          author: '张三',
          createTime: '2024-03-15 10:00:00',
          views: 1234,
          comments: 56,
          likes: 89,
          summary:
            '经过多年的选号经验总结，我发现了一些选号的小技巧，今天和大家分享一下...',
          isLiked: false,
        },
        // 更多帖子数据...
      ],
      currentPage: 1,
      pageSize: 10,
      total: 100,
      postDialogVisible: false,
      detailDialogVisible: false,
      newPost: {
        title: '',
        category: '',
        content: '',
      },
      postRules: {
        title: [
          { required: true, message: '请输入标题', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择分类', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入内容', trigger: 'blur' },
          { min: 10, max: 2000, message: '长度在 10 到 2000 个字符', trigger: 'blur' }
        ]
      },
      currentPost: {
        title: '',
        author: '',
        createTime: '',
        views: 0,
        comments: 0,
        likes: 0,
        content: '',
        commentList: [],
      },
      newComment: '',
    }
  },
  methods: {
    /**
     * 获取分类标签类型
     */
    getCategoryType(category) {
      const types = {
        experience: 'success',
        winning: 'warning',
        technical: 'info',
        other: '',
      }
      return types[category] || ''
    },

    /**
     * 获取分类标签文本
     */
    getCategoryLabel(category) {
      const labels = {
        experience: '选号经验',
        winning: '中奖分享',
        technical: '技术讨论',
        other: '其他',
      }
      return labels[category] || '其他'
    },

    /**
     * 格式化日期
     */
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD HH:mm')
    },

    /**
     * 显示发帖对话框
     */
    showPostDialog() {
      this.postDialogVisible = true
      this.newPost = {
        title: '',
        category: '',
        content: '',
      }
    },

    /**
     * 显示帖子详情
     */
    async showPostDetail(post) {
      try {
        // 模拟数据处理延迟
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // 模拟详细帖子数据
        this.currentPost = {
          ...post,
          content: post.summary + '\n\n这是详细内容。模拟生成的长文本内容，包含选号心得、技巧分享或中奖经历等。' +
                  '这只是一个示例文本，真实环境中应从服务器获取完整内容。',
          commentList: this.generateMockComments(post.id, post.comments)
        };
        
        this.detailDialogVisible = true;
      } catch (error) {
        this.$message.error('获取帖子详情失败，请稍后重试');
        console.error('获取帖子详情失败:', error);
      }
    },

    /**
     * 生成模拟评论数据
     */
    generateMockComments(postId, count) {
      const comments = [];
      const authors = ['用户A', '用户B', '用户C', '用户D', '用户E'];
      const contents = [
        '感谢分享，非常有用的信息！',
        '我也有类似的经验，确实如此。',
        '这个方法我试过，效果还不错。',
        '请问这种方法适用于所有情况吗？',
        '很详细的分析，学习了！'
      ];
      
      const commentsCount = Math.min(count, 10); // 最多生成10条评论
      
      for (let i = 0; i < commentsCount; i++) {
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30));
        
        comments.push({
          id: postId * 100 + i,
          author: authors[Math.floor(Math.random() * authors.length)],
          content: contents[Math.floor(Math.random() * contents.length)],
          createTime: date.toISOString()
        });
      }
      
      // 按时间排序
      return comments.sort((a, b) => new Date(b.createTime) - new Date(a.createTime));
    },

    /**
     * 处理点赞
     */
    async handleLike(post) {
      try {
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // 直接在本地切换点赞状态
        post.isLiked = !post.isLiked;
        post.likes += post.isLiked ? 1 : -1;
        
        this.$message.success(post.isLiked ? '点赞成功' : '已取消点赞');
      } catch (error) {
        this.$message.error('操作失败，请稍后重试');
        console.error('点赞操作失败:', error);
      }
    },

    /**
     * 提交新帖子
     */
    async submitPost() {
      try {
        // 表单验证
        await this.$refs.postForm.validate()
        
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 创建新帖子对象
        const newPost = {
          id: this.posts.length + 1,
          title: this.newPost.title,
          category: this.newPost.category,
          author: '当前用户',
          createTime: new Date().toISOString(),
          views: 0,
          comments: 0,
          likes: 0,
          summary: this.newPost.content.slice(0, 100) + (this.newPost.content.length > 100 ? '...' : ''),
          isLiked: false
        }
        
        // 添加到帖子列表最前面
        this.posts.unshift(newPost)
        
        this.$message.success('发布成功')
        this.postDialogVisible = false
      } catch (error) {
        if (error.message) {
          this.$message.error(error.message)
        } else {
          this.$message.error('发布失败，请稍后重试')
          console.error('发布帖子失败:', error)
        }
      }
    },

    /**
     * 提交评论
     */
    async submitComment() {
      try {
        // 校验评论内容
        if (!this.newComment.trim()) {
          this.$message.warning('请输入评论内容');
          return;
        }
        
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 创建新评论
        const newComment = {
          id: Date.now(),
          author: '当前用户',
          content: this.newComment,
          createTime: new Date().toISOString()
        };
        
        // 添加到评论列表
        this.currentPost.commentList.unshift(newComment);
        
        // 更新评论计数
        this.currentPost.comments += 1;
        
        this.$message.success('评论成功');
        this.newComment = '';
      } catch (error) {
        this.$message.error('评论失败，请稍后重试');
        console.error('提交评论失败:', error);
      }
    },

    /**
     * 获取帖子列表
     */
    async fetchPosts() {
      try {
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 模拟后端数据
        const mockPosts = [
          {
            id: 1,
            title: '双色球历史数据分析',
            content: '根据我对双色球近五年的数据分析，发现一些有趣的规律。首先，红球中最常出现的号码是...',
            author: '数据分析师',
            category: '数据分析',
            time: '2024-04-10',
            views: 328,
            likes: 42,
            comments: 15
          },
          {
            id: 2,
            title: '大乐透中奖经验分享',
            content: '上个月我用一套自己研发的选号系统选中了大乐透二等奖，想在这里分享一下我的选号心得...',
            author: '幸运儿',
            category: '经验分享',
            time: '2024-04-08',
            views: 489,
            likes: 78,
            comments: 32
          },
          {
            id: 3,
            title: '彩票投资心理学',
            content: '购买彩票时的心理状态会影响我们的选号。保持冷静和理性思考是成功的关键...',
            author: '心理学家',
            category: '理论探讨',
            time: '2024-04-05',
            views: 257,
            likes: 36,
            comments: 18
          },
          {
            id: 4,
            title: '号码优化算法讨论',
            content: '我开发了一种基于历史数据的号码优化算法，主要考虑号码的出现频率、间隔周期和组合规律...',
            author: '算法工程师',
            category: '技术讨论',
            time: '2024-04-03',
            views: 312,
            likes: 58,
            comments: 23
          },
          {
            id: 5,
            title: '新手购彩入门指南',
            content: '对于刚接触彩票的朋友，这里有一些基本的购彩知识和技巧，希望对你有所帮助...',
            author: '彩票顾问',
            category: '新手指南',
            time: '2024-04-01',
            views: 423,
            likes: 67,
            comments: 28
          }
        ];

        // 根据筛选条件处理数据
        let filteredPosts = [...mockPosts];
        
        // 类别筛选
        if (this.filter.category && this.filter.category !== '全部') {
          filteredPosts = filteredPosts.filter(post => post.category === this.filter.category);
        }
        
        // 搜索筛选
        if (this.filter.search) {
          const searchLower = this.filter.search.toLowerCase();
          filteredPosts = filteredPosts.filter(post => 
            post.title.toLowerCase().includes(searchLower) || 
            post.content.toLowerCase().includes(searchLower)
          );
        }
        
        // 排序
        if (this.filter.sort === 'newest') {
          filteredPosts.sort((a, b) => new Date(b.time) - new Date(a.time));
        } else if (this.filter.sort === 'hottest') {
          filteredPosts.sort((a, b) => b.views - a.views);
        } else if (this.filter.sort === 'mostLiked') {
          filteredPosts.sort((a, b) => b.likes - a.likes);
        }
        
        // 分页
        const total = filteredPosts.length;
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        const paginatedPosts = filteredPosts.slice(start, end);
        
        // 更新数据
        this.posts = paginatedPosts;
        this.total = total;
        
        this.$message.success('获取帖子列表成功');
      } catch (error) {
        this.$message.error('获取帖子列表失败，请稍后重试')
        console.error('获取帖子列表失败:', error)
      }
    },

    /**
     * 处理页码变化
     */
    handlePageChange(page) {
      this.currentPage = page
      this.fetchPosts()
    },
  },
  watch: {
    'filter.category'() {
      this.currentPage = 1
      this.fetchPosts()
    },
    'filter.sort'() {
      this.currentPage = 1
      this.fetchPosts()
    },
    'filter.search'() {
      this.currentPage = 1
      this.fetchPosts()
    },
  },
  mounted() {
    this.fetchPosts()
  },
}
</script>

<style lang="scss" scoped>
.discussion {
  .discussion-card {
    h2 {
      margin: 0;
      color: #303133;
    }

    .el-card__header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  .filter-section {
    margin-bottom: 20px;
  }

  .post-list {
    .post-card {
      margin-bottom: 20px;

      .post-header {
        margin-bottom: 15px;

        .post-title {
          display: flex;
          align-items: center;
          margin-bottom: 10px;

          h3 {
            margin: 0 10px 0 0;
            cursor: pointer;
            color: #303133;

            &:hover {
              color: #409eff;
            }
          }
        }

        .post-meta {
          color: #909399;
          font-size: 14px;

          span {
            margin-right: 20px;

            i {
              margin-right: 5px;
            }
          }
        }
      }

      .post-content {
        color: #606266;
        margin-bottom: 15px;
        line-height: 1.6;
      }

      .post-footer {
        display: flex;
        justify-content: flex-end;
        gap: 20px;
      }
    }
  }

  .pagination {
    margin-top: 20px;
    text-align: center;
  }

  .post-detail {
    .post-info {
      color: #909399;
      font-size: 14px;
      margin-bottom: 20px;

      span {
        margin-right: 20px;

        i {
          margin-right: 5px;
        }
      }
    }

    .post-content {
      color: #606266;
      line-height: 1.8;
      margin-bottom: 30px;
    }

    .comments-section {
      margin-top: 30px;
      border-top: 1px solid #ebeef5;
      padding-top: 20px;

      h4 {
        margin: 0 0 20px;
        color: #303133;
        font-size: 16px;
      }

      .comment-list {
        margin-bottom: 20px;

        .comment-item {
          padding: 15px;
          border-bottom: 1px solid #ebeef5;
          background-color: #fafafa;
          border-radius: 4px;
          margin-bottom: 10px;

          &:last-child {
            border-bottom: none;
          }

          .comment-header {
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;

            .comment-author {
              font-weight: bold;
              color: #303133;
            }

            .comment-time {
              color: #909399;
              font-size: 12px;
            }
          }

          .comment-content {
            color: #606266;
            line-height: 1.6;
            font-size: 14px;
            word-break: break-all;
          }
        }
      }

      .comment-form {
        margin-top: 20px;

        .el-textarea {
          margin-bottom: 10px;
          
          ::v-deep .el-textarea__inner {
            padding: 10px;
            line-height: 1.5;
            resize: none;
            background-color: #fafafa;
          }
        }

        .comment-form-footer {
          display: flex;
          justify-content: flex-end;
          margin-top: 10px;
        }
      }
    }
  }

  .post-form {
    padding: 20px;
    
    .el-form-item {
      margin-bottom: 20px;
    }
    
    .el-input,
    .el-select {
      width: 100%;
    }
    
    .el-textarea {
      font-size: 14px;
      
      ::v-deep .el-textarea__inner {
        padding: 10px;
        line-height: 1.5;
      }
    }
  }
  
  .dialog-footer {
    text-align: right;
    padding-top: 20px;
  }
}
</style>
