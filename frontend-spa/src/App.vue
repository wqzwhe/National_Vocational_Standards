<template>
  <div class="page">
    <div class="section" style="padding:12px">
      <div class="brand-hero animate-in fade-in duration-300">
        <div class="pattern-bg bg-grid"></div>
        <div class="brand-line">
        <div class="brand">
          <span class="accent-dot"></span>
          <div class="title">国家职业标准检索与下载</div>
        </div>
        <div class="brand-controls">
          <select v-model="mode" class="theme-select inline-flex items-center rounded-lg border border-slate-300 bg-white/90 px-2 py-1 text-sm text-slate-800 shadow dark:bg-white/10 dark:border-white/10 dark:text-slate-100" @change="applyTheme">
            <option value="auto">自动</option>
            <option value="light">亮色</option>
            <option value="dark">暗色</option>
          </select>
        </div>
        </div>
      </div>
    </div>
    <div class="content">
      <search-list />
    </div>
    <div class="footer-banner section">
      <div class="footer-inner">
        <div class="footer-content">
          <span class="accent-dot"></span>
          <a href="https://www.wzhcn.cn" target="_blank" rel="noopener" class="home-link">www.wzhcn.cn</a>
          <i v-if="isHttps" class="el-icon-lock https-icon"></i>
          <span class="sep">·</span>
          <span>始于 2017年</span>
          <span class="sep">·</span>
          <a href="https://beian.miit.gov.cn" target="_blank" rel="noopener" class="icp">浙ICP备17057070号</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchList from './components/SearchList.vue'
export default {
  components: { SearchList },
  computed: {
    isHttps() {
      return typeof window !== 'undefined' && window.location && window.location.protocol === 'https:'
    }
  },
  data() {
    return { dark: false, mode: 'auto', mediaQuery: null, themeOptions: [
      { label: '自动', value: 'auto' },
      { label: '亮色', value: 'light' },
      { label: '暗色', value: 'dark' }
    ] }
  },
  mounted() {
    const saved = typeof localStorage !== 'undefined' ? localStorage.getItem('themeMode') : null
    if (saved) this.mode = saved
    if (typeof window !== 'undefined' && window.matchMedia) {
      this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      if (this.mediaQuery.addEventListener) {
        this.mediaQuery.addEventListener('change', () => this.applyTheme())
      }
    }
    this.applyTheme()
  },
  methods: {
    applyTheme() {
      if (typeof document !== 'undefined') {
        let useDark = false
        if (this.mode === 'auto') {
          useDark = this.mediaQuery ? this.mediaQuery.matches : false
        } else if (this.mode === 'dark') {
          useDark = true
        } else {
          useDark = false
        }
        this.dark = useDark
        document.body.classList.toggle('theme-dark', useDark)
        document.documentElement.classList.toggle('dark', useDark)
        if (typeof localStorage !== 'undefined') localStorage.setItem('themeMode', this.mode)
      }
    }
  }
}
</script>

<style>
:root { --primary:#2563eb; --accent:#0ea5e9; --text:#1f2937; --muted:#6b7280 }
body { margin:0; background: linear-gradient(135deg, #f6f7fb 0%, #eef1f8 50%, #e8f5ff 100%); color:var(--text) }
.page { max-width: 1120px; margin: 0 auto; padding: 20px; min-height: 100vh; display:flex; flex-direction: column }
.content { flex: 1; padding-bottom: 72px }
.brand-line { display:flex; align-items:center; justify-content:space-between }
.brand { display:flex; align-items:center; gap:12px }
.brand .title { font-size: 22px; font-weight: 700; letter-spacing:.5px }
.brand-hero { position: relative; overflow:hidden; border-radius:12px; transition: transform .2s ease, box-shadow .2s ease }
.brand-hero:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(17,24,39,.18) }
.theme-dark .brand-hero:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,0,0,.38) }
.pattern-bg { position:absolute; inset:0; pointer-events:none }
.section { background: rgba(255,255,255,.85); border-radius:16px; box-shadow: 0 10px 30px rgba(17,24,39,.08); backdrop-filter: saturate(160%) blur(6px) }
.footer-banner { position: fixed; left:0; right:0; bottom:0; margin:0; z-index:1000; border-radius:0; background: linear-gradient(180deg, rgba(255,255,255,.72), rgba(255,255,255,.58)); backdrop-filter: saturate(180%) blur(12px); box-shadow: 0 -8px 22px rgba(17,24,39,.12); border-top: 1px solid rgba(67,56,202,.08) }
.footer-inner { max-width: 1120px; margin:0 auto; display:flex; align-items:center; justify-content:center; padding:12px }
.footer-content { display:flex; align-items:center; gap:12px; padding:10px 16px; border-radius:9999px; background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.78)); border: 1px solid rgba(79,70,229,.18); box-shadow: 0 4px 12px rgba(79,70,229,.08); color:var(--muted); font-size:14px; letter-spacing:.2px; transition: all .2s ease }
.footer-content:hover { transform: translateY(-1px); box-shadow: 0 8px 22px rgba(79,70,229,.12) }
.accent-dot { width:8px; height:8px; border-radius:50%; background: linear-gradient(135deg, var(--primary), var(--accent)); box-shadow: 0 0 0 4px rgba(79,70,229,.12) }
.footer-content .home-link { background: linear-gradient(90deg, var(--primary), var(--accent)); -webkit-background-clip: text; background-clip: text; color: transparent; font-weight:700; text-decoration: none }
.footer-content .home-link:hover { text-decoration: underline }
.footer-content .sep { color:#c0c4cc }
.footer-content .icp { color:#80828a; text-decoration: none }
.https-icon { color:#10b981; font-size:14px }

.theme-dark { --text:#e5e7eb; --muted:#9aa3af; --primary:#5b7cfa; --accent:#38bdf8 }
body.theme-dark { background: linear-gradient(135deg, #0b1220 0%, #0f1628 50%, #0f1b2d 100%); color:var(--text) }
.theme-dark .section { background: rgba(17,24,39,.78); box-shadow: 0 10px 30px rgba(0,0,0,.28) }
.theme-dark .footer-banner { background: linear-gradient(180deg, rgba(17,24,39,.78), rgba(17,24,39,.62)); border-top: 1px solid rgba(79,70,229,.24); box-shadow: 0 -8px 22px rgba(0,0,0,.32) }
.theme-dark .footer-content { background: linear-gradient(180deg, rgba(17,24,39,.92), rgba(17,24,39,.84)); border: 1px solid rgba(79,70,229,.28); color:#cbd5e1 }
.theme-dark .footer-content .sep { color:#64748b }
.theme-dark .footer-content .icp { color:#9aa3af }
@media (max-width: 600px) {
  .footer-inner { padding: 8px }
  .footer-content { gap:8px; padding:8px 12px; font-size:12px }
  .content { padding-bottom: 56px }
}

.el-card { background: linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.88)); border-color: rgba(79,70,229,.12) }
.theme-dark .el-card { background: linear-gradient(180deg, rgba(17,24,39,.92), rgba(17,24,39,.86)); border-color: rgba(255,255,255,.12) }
.theme-dark .el-card.is-hover-shadow { box-shadow: 0 8px 22px rgba(0,0,0,.35) }
.theme-dark .el-card__body { color: var(--text) }
.card-item.el-card { background: linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.88)); border-color: rgba(79,70,229,.12) }
.card-item .el-card__body { background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.82)); border: 1px solid rgba(79,70,229,.12); border-radius:12px; box-shadow: 0 4px 12px rgba(17,24,39,.08) }
.theme-dark .card-item.el-card { background: linear-gradient(180deg, rgba(17,24,39,.94) 0%, rgba(17,24,39,.84) 100%) !important; border-color: rgba(255,255,255,.12) !important; box-shadow: inset 0 0 0 1px rgba(255,255,255,.06), 0 8px 22px rgba(0,0,0,.35) !important }
.theme-dark .card-item .el-card__body { background: linear-gradient(180deg, rgba(17,24,39,.94) 0%, rgba(17,24,39,.86) 100%) !important; border: 1px solid rgba(79,70,229,.24) !important; box-shadow: inset 0 0 12px rgba(79,70,229,.10), 0 4px 16px rgba(0,0,0,.28) !important; color: var(--text) }
.theme-dark .el-button { color:#e5e7eb; background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.12) }
.theme-dark .el-button:hover { background: rgba(255,255,255,.12); border-color: rgba(255,255,255,.18) }
.theme-dark .el-button--primary { background:#6366f1; border-color:#6366f1; color:#fff }
.theme-dark .el-button--primary:hover { background:#585df0; border-color:#585df0 }
.theme-dark .el-input__inner { background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.12); color:#e5e7eb }
.theme-dark .el-input__inner::placeholder { color:#9aa3af }
.theme-dark .el-input.is-active .el-input__inner,
.theme-dark .el-input__inner:focus { border-color:#6366f1; box-shadow:none }
.theme-dark .el-select .el-input__inner { background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.12); color:#e5e7eb }
.theme-dark .el-select-dropdown { background: rgba(17,24,39,.98); border-color: rgba(255,255,255,.12); color:#e5e7eb }
.theme-dark .el-select-dropdown__item:hover { background: rgba(255,255,255,.06) }
.theme-dark .el-pagination { color:#cbd5e1 }
.theme-dark .el-pagination button { background: transparent; color:#cbd5e1 }
.theme-dark .el-pagination .el-pager li { background: transparent; color:#cbd5e1 }
.theme-dark .el-pagination .el-pager li.active { background:#4f46e5; color:#fff; border-radius:6px }
.theme-dark .el-tag { background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.12); color:#cbd5e1 }
.theme-dark .el-alert { background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.12); color:#e5e7eb }
.theme-dark .el-dialog { background: rgba(17,24,39,.92); border: 1px solid rgba(255,255,255,.12); color:#e5e7eb }
.theme-dark .el-dialog__header { border-bottom: 1px solid rgba(255,255,255,.06) }
.theme-dark .el-dialog__title { color:#e5e7eb }
</style>
