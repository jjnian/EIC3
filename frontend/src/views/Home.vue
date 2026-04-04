<template>
  <div class="home">
    <div class="hero">
      <h1>OntologyFlow</h1>
      <p>本体关系分析平台</p>
      <p class="subtitle">从图片、视频、文字中提取实体与关系，构建知识图谱</p>
      <div class="actions">
        <el-button type="primary" size="large" @click="$router.push('/register')">
          开始使用
        </el-button>
        <el-button size="large" @click="$router.push('/login')">
          登录
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero {
  text-align: center;
  color: white;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.hero p {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem !important;
  opacity: 0.9;
  margin-bottom: 2rem !important;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
</style>