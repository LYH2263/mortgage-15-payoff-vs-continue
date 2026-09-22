<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const principal = ref(800000)
const annual_rate = ref(4.2)
const months = ref(360)
const paid_periods = ref(60)
const out = ref(null)
const cmp = ref(null)
const err = ref('')

const call = async (path, body) => {
  err.value = ''
  try { return await postJSON(path, body) }
  catch (e) { err.value = '请求失败：已过期数须在 1 到 总期数-1 之间'; return null }
}
const run = async () => { out.value = await call('/api/schedule', { principal: principal.value, annual_rate: annual_rate.value, months: months.value, persist: true }) }
// 默认只试算，不写记录
const trial = async () => { cmp.value = await call('/api/settle-compare', { principal: principal.value, annual_rate: annual_rate.value, months: months.value, paid_periods: paid_periods.value, persist: false }) }
// persist=true 写入一条对照记录，钉选 P 与三项金额
const save = async () => { cmp.value = await call('/api/settle-compare', { principal: principal.value, annual_rate: annual_rate.value, months: months.value, paid_periods: paid_periods.value, persist: true }) }
</script>
<template><div class="page"><h1>等额本息试算</h1>
<label>本金 <input v-model.number="principal" /></label>
<label>年利率% <input v-model.number="annual_rate" /></label>
<label>月数 <input v-model.number="months" /></label>
<button @click="run">计算</button>
<p v-if="out">月供 {{ out.monthly_payment }} · 利息合计 {{ out.total_interest }}</p>

<h2>结清 / 续还对照</h2>
<label>已过期数 P（1 ~ {{ months - 1 }}） <input v-model.number="paid_periods" /></label>
<button @click="trial">试算对照</button>
<button @click="save">保存对照</button>
<p v-if="err" style="color:#b00020">{{ err }}</p>
<table v-if="cmp">
  <tr><th>钉选时点</th><td>第 {{ cmp.paid_periods }} 期末</td></tr>
  <tr><th>剩余本金（一次性结清余额）</th><td>{{ cmp.remaining_principal }}</td></tr>
  <tr><th>续还剩余利息合计</th><td>{{ cmp.remaining_interest }}</td></tr>
  <tr><th>一次性结清只需偿还</th><td>{{ cmp.settle_amount }}</td></tr>
  <tr><th>续还相对结清的超额利息</th><td>{{ cmp.extra_interest }}</td></tr>
  <tr v-if="cmp.run_id"><th>对照记录</th><td>#{{ cmp.run_id }}（已保存）</td></tr>
</table>
</div></template>
