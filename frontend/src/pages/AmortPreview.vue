<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const out = ref(null)
const paid_periods = ref(120)
const cmp = ref(null)
const err = ref('')
const load = async () => { out.value = await postJSON('/api/schedule', { principal: 1000000, annual_rate: 3.5, months: 360, persist: false, preview_rows: 12 }) }
load()
// 摊还预览上直接试算结清/续还对照，默认不落记录
const compare = async () => {
  err.value = ''
  try { cmp.value = await postJSON('/api/settle-compare', { principal: 1000000, annual_rate: 3.5, months: 360, paid_periods: paid_periods.value, persist: false }) }
  catch (e) { err.value = '请求失败：已过期数须在 1 到 359 之间'; cmp.value = null }
}
</script>
<template><div class="page"><h1>摊还表预览</h1>
<table v-if="out"><tr v-for="r in out.preview" :key="r.period"><td>第{{ r.period }}期</td><td>{{ r.payment }}</td><td>{{ r.balance }}</td></tr></table>
<h2>结清 / 续还对照</h2>
<label>已过期数 P（1 ~ 359） <input v-model.number="paid_periods" /></label>
<button @click="compare">试算对照</button>
<p v-if="err" style="color:#b00020">{{ err }}</p>
<table v-if="cmp">
  <tr><th>钉选时点</th><td>第 {{ cmp.paid_periods }} 期末</td></tr>
  <tr><th>剩余本金（一次性结清余额）</th><td>{{ cmp.remaining_principal }}</td></tr>
  <tr><th>续还剩余利息合计</th><td>{{ cmp.remaining_interest }}</td></tr>
  <tr><th>一次性结清只需偿还</th><td>{{ cmp.settle_amount }}</td></tr>
  <tr><th>续还相对结清的超额利息</th><td>{{ cmp.extra_interest }}</td></tr>
</table>
</div></template>
