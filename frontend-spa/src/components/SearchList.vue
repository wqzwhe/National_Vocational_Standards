<template>
  <div class="section" style="margin-top:12px; position:relative">
    <div v-if="loading" class="loading-overlay"><div class="spinner" /></div>
    <div v-if="!started" class="hero animate-in fade-in slide-in-from-bottom duration-300">
      <div class="hero-title">国家职业标准检索</div>
      <RainbowButton class="hero-btn animate-in zoom-in duration-300" size="lg" @click="startSearch">开始搜索</RainbowButton>
    </div>
    <div v-else>
    <div class="toolbar">
      <HaloSearch class="grow" v-model="q" placeholder="请输入职业名称，例如：起重" @enter="openCaptchaDialog" />
      <select v-model.number="pagination.pageSize" class="w-[120px] shrink-0 rounded-lg border border-slate-300 bg-white/95 px-2 py-2 text-slate-800 shadow dark:bg-white/10 dark:border-white/10 dark:text-slate-100" @change="onPageSizeChange">
        <option :value="9">9</option>
        <option :value="27">27</option>
        <option :value="81">81</option>
      </select>
      <RainbowButton class="shrink-0" size="md" @click="openCaptchaDialog">搜索</RainbowButton>
    </div>


    <div style="margin:10px" class="muted">共 {{ pagination.total }} 条记录</div>

    

    <div class="mobile-only" style="padding:12px">
      <div v-if="items.length === 0" class="ui-empty animate-in fade-in duration-200">{{ emptyText }}</div>
      <div v-else class="pattern-cards animate-in fade-in duration-200">
        <div class="pattern-bg bg-grid"></div>
        <div class="card-grid">
        <CardContainer :class="['animate-in','fade-in','slide-in-from-bottom','duration-300', delayClass(i)]" v-for="(it, i) in items" :key="it.id || it.code" :style="{ willChange: 'transform, opacity' }">
          <CardBody class="card-item">
            <CardItem as="div" :translateZ="z.title" class="card-title">{{ it.name }}</CardItem>
            <CardItem as="div" :translateZ="z.code" class="muted code" style="margin-top:6px">{{ it.code }}</CardItem>
            <CardItem as="div" :translateZ="z.meta" class="muted meta-line" style="margin-top:6px">{{ it.issueNumber }} · {{ it.issueTime }}</CardItem>
            <CardItem as="div" :translateZ="z.name" class="file-name">{{ it.standardInfoName }}</CardItem>
            <CardItem as="div" :translateZ="z.actions" class="card-actions">
              <RainbowButton size="sm" :disabled="!it.downloadUrl" @click="openDownload(it)">下载</RainbowButton>
              <button class="bg-gradient-to-r from-indigo-600 to-sky-400 bg-clip-text text-transparent text-xs" :disabled="!it.downloadUrl" @click="copyDownload(it)">复制链接</button>
            </CardItem>
          </CardBody>
        </CardContainer>
        </div>
      </div>
    </div>

    <div v-if="pagination.total > 0" style="padding:12px;border-top:1px solid #ebeef5">
      <nav class="ui-pagination flex items-center gap-2 animate-in fade-in duration-200">
        <RainbowButton class="pg-btn animate-in fade-in slide-in-from-bottom duration-200" size="sm" :disabled="pagination.pageNum<=1" @click="setPage(pagination.pageNum-1)">上一页</RainbowButton>
        <div class="pg-pages flex gap-1">
          <button v-for="(p, i) in pages" :key="p" :class="['pg-page rounded-md border px-2 py-1 text-sm transition','animate-in','fade-in','slide-in-from-bottom','duration-200', delayClass(i), (p===pagination.pageNum ? 'bg-indigo-600 text-white border-indigo-600' : 'border-slate-300 bg-white/95 text-slate-800 dark:bg-white/10 dark:border-white/10 dark:text-slate-100')]" :style="{ willChange: 'transform, opacity' }" @click="setPage(p)">{{ p }}</button>
        </div>
        <RainbowButton class="pg-btn animate-in fade-in slide-in-from-bottom duration-200" size="sm" :disabled="pagination.pageNum>=pageCount" @click="setPage(pagination.pageNum+1)">下一页</RainbowButton>
      </nav>
    </div>
    <div v-if="captchaVisible" class="fixed inset-0 bg-black/35 flex items-center justify-center z-[1000] animate-in fade-in duration-200">
      <div class="w-[360px] max-w-[calc(100%-24px)] rounded-xl border border-slate-300 bg-white/98 shadow-xl dark:bg-slate-900/90 dark:border-white/10 dark:text-slate-100 animate-in zoom-in scale-in duration-300" @click.stop>
        <div class="px-4 py-3 border-b border-slate-200 dark:border-white/10 font-bold">验证码</div>
        <div class="p-4">
          <div style="margin-bottom:12px;display:flex;align-items:center;gap:10px">
            <img :src="captchaImage" alt="captcha" style="height:60px;border:1px solid #ebeef5;border-radius:4px" />
            <a class="ui-link" @click.prevent="refreshCaptcha">看不清，换一张</a>
          </div>
          <input v-model="captchaInput" placeholder="请输入验证码" ref="captchaInput" class="w-full rounded-lg border border-slate-300 bg-white/95 px-3 py-2 text-slate-800 shadow focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-white/10 dark:border-white/10 dark:text-slate-100" />
        </div>
        <div class="px-4 py-3 border-t border-slate-200 dark:border-white/10 flex gap-2 justify-end">
          <RainbowButton @click="captchaVisible=false">取消</RainbowButton>
          <RainbowButton @click="confirmCaptcha">确定</RainbowButton>
        </div>
      </div>
    </div>
    <div v-if="toastVisible" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[1100] animate-in fade-in slide-in-from-bottom duration-200">
      <div :class="toastClass" class="px-3 py-2 rounded-lg shadow-lg text-sm">{{ toastMsg }}</div>
    </div>
    </div>
  </div>
  
</template>

<script>
import RainbowButton from './ui/RainbowButton.vue'
import HaloSearch from './ui/HaloSearch.vue'
import CardContainer from './ui/cards/CardContainer.vue'
import CardBody from './ui/cards/CardBody.vue'
import CardItem from './ui/cards/CardItem.vue'
export default {
  name: 'SearchList',
  components: { RainbowButton, HaloSearch, CardContainer, CardBody, CardItem },
  data() {
    return { started: false, q: '', loading: false, errorMsg: '', items: [], pagination: { pageNum: 1, pageSize: 9, total: 0, pages: 0 }, captchaVisible: false, captchaId: '', captchaImage: '', captchaInput: '', pageSizeOptions: [ {label:'10', value:10}, {label:'20', value:20}, {label:'50', value:50} ], toastVisible: false, toastMsg: '', toastType: 'info', toastTimer: null, mobile: false }
  },
  computed: {
    emptyText() {
      if (this.loading) return '加载中...'
      if (this.errorMsg) return '请求失败'
      return '未找到相关职业'
    },
    isDark() {
      if (typeof document === 'undefined') return false
      const b = document.body.classList.contains('theme-dark')
      const r = document.documentElement.classList.contains('dark')
      return b || r
    },
    pageCount() { return Math.max(1, Math.ceil(this.pagination.total / this.pagination.pageSize)) },
    pages() {
      const count = this.pageCount
      const cur = this.pagination.pageNum
      const span = 7
      const start = Math.max(1, cur - Math.floor(span/2))
      const end = Math.min(count, start + span - 1)
      const s = Math.max(1, end - span + 1)
      return Array.from({length: end - s + 1}, (_, i) => s + i)
    },
    toastClass() {
      if (this.toastType === 'success') return 'bg-emerald-600 text-white'
      if (this.toastType === 'error') return 'bg-rose-600 text-white'
      if (this.toastType === 'warning') return 'bg-amber-500 text-white'
      return 'bg-slate-800 text-white'
    },
    z() {
      if (this.mobile) {
        return { title: 24, code: 14, meta: 12, name: 18, actions: 20 }
      }
      return { title: 36, code: 20, meta: 16, name: 24, actions: 28 }
    }
  },
  mounted() {
    if (typeof window !== 'undefined' && window.matchMedia) {
      const mq = window.matchMedia('(max-width: 600px)')
      this.mobile = mq.matches
      if (mq.addEventListener) mq.addEventListener('change', e => { this.mobile = e.matches })
    }
  },
  methods: {
    startSearch() { this.started = true },
    delayClass(i) {
      const idx = i % 8
      const map = ['delay-100','delay-150','delay-200','delay-300','delay-500','delay-700','delay-1000','delay-1000']
      return map[idx]
    },
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
        this.$nextTick(() => { const el = this.$refs.captchaInput; if (el && el.focus) el.focus() })
      } catch (e) {
        this.errorMsg = '验证码获取失败'
        this.showToast('验证码获取失败', 'error')
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
        this.errorMsg = '验证码获取失败'
      }
    },
    async confirmCaptcha() {
      if (!this.captchaInput) { this.errorMsg = '请输入验证码答案'; this.showToast('请输入验证码答案', 'warning'); return }
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
              this.errorMsg = '验证码错误或已过期'
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
    setPage(p) { this.pagination.pageNum = Math.max(1, Math.min(p, this.pageCount)); this.doSearch() },
    onPageSizeChange() { this.pagination.pageNum = 1; this.doSearch() },
    openDownload(it) {
      if (!it || !it.downloadUrl) return
      const a = document.createElement('a')
      a.href = it.downloadUrl
      a.target = '_blank'
      a.download = it.standardInfoName || ''
      a.click()
    },
    async copyDownload(it) {
      const u = it && it.downloadUrl
      if (!u) { this.errorMsg = '暂无下载链接'; this.showToast('暂无下载链接', 'warning'); return }
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(u)
        } else {
          const ta = document.createElement('textarea')
          ta.value = u
          document.body.appendChild(ta)
          ta.select()
          document.execCommand('copy')
          document.body.removeChild(ta)
        }
        this.errorMsg = '链接已复制'
        this.showToast('链接已复制', 'success')
      } catch (e) {
        this.errorMsg = '复制失败'
        this.showToast('复制失败', 'error')
      }
    },
    showToast(msg, type = 'info') {
      this.toastMsg = msg
      this.toastType = type
      this.toastVisible = true
      if (this.toastTimer) clearTimeout(this.toastTimer)
      this.toastTimer = setTimeout(() => { this.toastVisible = false }, 2000)
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
.muted { color: var(--muted) }
.card-title { font-weight:700; color: var(--text); font-size:16px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
.file-name { margin-top:8px; color: var(--text); overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
.card-actions { margin-top: auto; display:flex; align-items:flex-end; padding-top:6px; flex-shrink:0; gap:8px; flex-wrap:wrap }
.desktop-only { display:block }
.mobile-only { display:block }
@media (max-width: 600px) { .desktop-only { display:block } .mobile-only { display:block } }
.pattern-cards { position:relative; overflow:hidden; border-radius:12px }
.pattern-cards .pattern-bg { position:absolute; inset:0; pointer-events:none }
.card-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:12px; align-items: stretch }
.card-item { margin: 0; height: 100%; overflow:hidden; background: linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.88)); border: 1px solid rgba(79,70,229,.12); border-radius:12px; box-shadow: 0 4px 12px rgba(17,24,39,.08); padding:12px; display:flex; flex-direction:column; transition: transform .2s ease, box-shadow .2s ease }
.card-item:hover { box-shadow: 0 8px 22px rgba(17,24,39,.18) }
.theme-dark .card-item { background: linear-gradient(180deg, rgba(17,24,39,.92), rgba(17,24,39,.86)); border: 1px solid rgba(255,255,255,.12); box-shadow: 0 4px 16px rgba(0,0,0,.28) }
.theme-dark .card-item:hover { box-shadow: 0 10px 28px rgba(0,0,0,.38) }
.theme-dark .card-title { color:#f5f7ff; text-shadow: 0 0 6px rgba(91,124,250,.35), 0 0 1px rgba(255,255,255,.35) }
.card-actions { margin-top:auto; padding-top:6px }
.ui-empty { padding:24px; text-align:center; color: var(--muted) }
.ui-alert { padding:10px 12px; border-radius:8px; border:1px solid rgba(79,70,229,.18); background: rgba(255,255,255,.96); color:#b91c1c }
.ui-alert.error { border-color:#ef4444; background: rgba(255,0,0,.06) }
.ui-link { color: var(--primary); text-decoration: underline; cursor: pointer }
.loading-overlay { position:absolute; inset:0; background: rgba(255,255,255,.45); backdrop-filter: blur(4px); display:flex; align-items:center; justify-content:center; z-index:10 }
.spinner { width:24px; height:24px; border-radius:50%; border:3px solid #cbd5e1; border-top-color: var(--primary); animation: spin .8s linear infinite }
@keyframes spin { to { transform: rotate(360deg) } }
.code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
.meta-line { overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
</style>