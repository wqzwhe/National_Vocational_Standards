<template>
  <el-card shadow="never" class="section" :body-style="{padding:'0'}" style="margin-top:12px" v-loading="loading">
    <div v-if="!started" class="hero">
      <div class="hero-title">国家职业标准检索</div>
      <el-button type="primary" icon="el-icon-search" class="hero-btn" @click="startSearch">开始搜索</el-button>
    </div>
    <div v-else>
    <div class="toolbar">
      <el-input v-model="q" placeholder="请输入职业名称，例如：起重" clearable class="grow" @keyup.enter.native="openCaptchaDialog" />
      <el-select v-model="pagination.pageSize" placeholder="每页数量" style="width:120px" @change="onPageSizeChange">
        <el-option :value="10" label="10" />
        <el-option :value="20" label="20" />
        <el-option :value="50" label="50" />
      </el-select>
      <el-button type="primary" icon="el-icon-search" @click="openCaptchaDialog">搜索</el-button>
    </div>

    <div v-if="errorMsg" style="padding:0 12px 12px 12px">
      <el-alert :title="errorMsg" type="error" show-icon />
    </div>

    <div style="margin:10px" class="muted">共 {{ pagination.total }} 条记录</div>

    

    <div class="mobile-only" style="padding:12px">
      <el-empty v-if="items.length === 0" :description="emptyText" />
      <div v-else class="card-grid">
        <el-card v-for="it in items" :key="it.id || it.code" class="card-item" shadow="hover">
          <div style="font-weight:600">{{ it.name }}</div>
          <div class="muted code" style="margin-top:6px">{{ it.code }}</div>
          <div class="muted" style="margin-top:6px">{{ it.issueNumber }} · {{ it.issueTime }}</div>
          <div style="margin-top:8px">{{ it.standardInfoName }}</div>
          <div style="margin-top:10px">
            <el-button type="success" size="mini" :disabled="!it.downloadUrl" @click="openDownload(it)">下载</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <div v-if="pagination.total > 0" style="padding:12px;border-top:1px solid #ebeef5">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        :current-page.sync="pagination.pageNum"
        @current-change="onPageChange"
      />
    </div>
    <el-dialog title="验证码" :visible.sync="captchaVisible" width="360px" :close-on-click-modal="false" :close-on-press-escape="false" append-to-body>
      <div style="margin-bottom:12px;display:flex;align-items:center;gap:10px">
        <img :src="captchaImage" alt="captcha" style="height:60px;border:1px solid #ebeef5;border-radius:4px" />
        <el-link type="primary" @click="refreshCaptcha">看不清，换一张</el-link>
      </div>
      <el-input v-model="captchaInput" placeholder="请输入验证码" ref="captchaInput" />
      <span slot="footer" class="dialog-footer">
        <el-button @click="captchaVisible=false">取消</el-button>
        <el-button type="primary" @click="confirmCaptcha">确定</el-button>
      </span>
    </el-dialog>
    </div>
  </el-card>
  
</template>

<script>
export default {
  name: 'SearchList',
  data() {
    return { started: false, q: '', loading: false, errorMsg: '', items: [], pagination: { pageNum: 1, pageSize: 10, total: 0, pages: 0 }, captchaVisible: false, captchaId: '', captchaImage: '', captchaInput: '' }
  },
  computed: {
    emptyText() {
      if (this.loading) return '加载中...'
      if (this.errorMsg) return '请求失败'
      return '未找到相关职业'
    }
  },
  mounted() {},
  methods: {
    startSearch() { this.started = true },
    async openCaptchaDialog() {
      const kw = this.q.trim()
      if (!kw) { this.errorMsg = '请输入关键词'; return }
      this.captchaInput = ''
      try {
        const r = await fetch('/api/captcha/new')
        if (!r.ok) throw new Error('captcha_failed')
        const data = await r.json()
        const body = data.body || {}
        this.captchaId = body.id || ''
        this.captchaImage = body.image || ''
        this.captchaVisible = true
        this.$nextTick(() => { if (this.$refs.captchaInput) this.$refs.captchaInput.focus() })
      } catch (e) {
        this.errorMsg = '验证码获取失败'
      }
    },
    async refreshCaptcha() {
      try {
        const r = await fetch('/api/captcha/new')
        if (!r.ok) throw new Error('captcha_failed')
        const data = await r.json()
        const body = data.body || {}
        this.captchaId = body.id || ''
        this.captchaImage = body.image || ''
        this.captchaInput = ''
        this.captchaVisible = true
        this.$nextTick(() => { if (this.$refs.captchaInput) this.$refs.captchaInput.focus() })
      } catch (e) {
        this.$message.error('验证码获取失败')
      }
    },
    async confirmCaptcha() {
      if (!this.captchaInput) { this.$message.error('请输入验证码答案'); return }
      this.captchaVisible = false
      await this.doSearch()
    },
    async doSearch() {
      this.loading = true
      this.errorMsg = ''
      try {
        const kw = this.q.trim()
        if (!kw) { this.errorMsg = '请输入关键词'; this.loading = false; return }
        if (!this.captchaId || !this.captchaInput) { this.loading = false; this.openCaptchaDialog(); return }
        const url = `/api/search?q=${encodeURIComponent(kw)}&pageNum=${this.pagination.pageNum}&pageSize=${this.pagination.pageSize}&captchaId=${encodeURIComponent(this.captchaId)}&captchaAnswer=${encodeURIComponent(this.captchaInput)}`
        const r = await fetch(url)
        if (!r.ok) {
          if (r.status === 400) {
            const d = await r.json().catch(() => ({}))
            if (d && (d.msg === 'captcha_invalid' || d.msg === 'captcha_required')) {
              this.$message.error('验证码错误或已过期')
              this.loading = false
              this.refreshCaptcha()
              return
            }
          }
          throw new Error('network_error')
        }
        const data = await r.json()
        const body = data.body || {}
        const prefix = 'http://osta.mohrss.gov.cn/api/sys/downloadFile/decrypt?fileName='
        const sanitizeUrl = u => typeof u === 'string' ? u.replace(/`/g, '').trim() : ''
        const list = Array.isArray(body.list) ? body.list : []
        this.items = list.map(it => {
          const raw = sanitizeUrl(it.downloadUrl)
          const dl = raw || (it.standardInfo ? `${prefix}${it.standardInfo}` : '')
          const time = typeof it.issueTime === 'string' ? it.issueTime.split(' ')[0] : ''
          return { ...it, downloadUrl: dl, issueTime: time }
        })
        this.pagination.total = Number(body.total || (this.items ? this.items.length : 0))
        this.pagination.pages = Number(body.pages || 0)
        if (body.pageNum) this.pagination.pageNum = Number(body.pageNum)
      } catch (e) {
        this.errorMsg = '数据请求失败，请稍后重试'
        this.items = []
        this.pagination.total = 0
        this.pagination.pages = 0
      } finally {
        this.loading = false
      }
    },
    onPageChange(p) { this.pagination.pageNum = p; this.doSearch() },
    onPageSizeChange() { this.pagination.pageNum = 1; this.doSearch() },
    openDownload(it) {
      if (!it || !it.downloadUrl) return
      const a = document.createElement('a')
      a.href = it.downloadUrl
      a.target = '_blank'
      a.download = it.standardInfoName || ''
      a.click()
    }
  }
}
</script>

<style scoped>
.hero { min-height: 60vh; display:flex; flex-direction:column; align-items:center; justify-content:center }
.hero-title { font-size: 28px; font-weight: 700; margin-bottom: 16px }
.hero-btn { font-size: 20px; padding: 14px 28px }
.toolbar { display:flex; gap:8px; flex-wrap:wrap; padding:12px }
.toolbar .grow { flex: 1 }
.muted { color:#909399 }
.desktop-only { display:block }
.mobile-only { display:block }
@media (max-width: 600px) { .desktop-only { display:block } .mobile-only { display:block } }
.card-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:12px }
.card-item { margin: 0 }
.code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace }
</style>