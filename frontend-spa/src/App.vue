<template>
  <div class="page">
    <el-card shadow="always" class="section" :body-style="{padding:'12px'}">
      <div class="brand">
        <i class="el-icon-document" style="color:var(--primary);font-size:20px"></i>
        <div class="title">国家职业标准检索与下载</div>
      </div>
    </el-card>
    <search-list />
  </div>
</template>

<script>
import SearchList from './components/SearchList.vue'
export default { components: { SearchList } }
</script>

<style>
:root { --primary:#4f46e5; --accent:#22d3ee }
body { margin:0; background: linear-gradient(135deg, #f6f7fb 0%, #eef1f8 50%, #e8f5ff 100%); color:#1f2937 }
.page { max-width: 1120px; margin: 0 auto; padding: 20px }
.brand { display:flex; align-items:center; gap:12px }
.brand .title { font-size: 22px; font-weight: 700; letter-spacing:.5px }
.section { background: rgba(255,255,255,.85); border-radius:16px; box-shadow: 0 10px 30px rgba(17,24,39,.08); backdrop-filter: saturate(160%) blur(6px) }
</style>