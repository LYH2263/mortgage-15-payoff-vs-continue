<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const principal = ref(800000)
const annual_rate = ref(4.2)
const months = ref(360)
const elapsed = ref(36)
const persist = ref(false)
const out = ref(null)
const cmp = ref(null)
const cmpErr = ref('')
const run = async () => { out.value = await postJSON('/api/schedule', { principal: principal.value, annual_rate: annual_rate.value, months: months.value, persist: true }) }
const compare = async () => {
  cmp.value = null; cmpErr.value = ''
  try {
    cmp.value = await postJSON('/api/payoff-compare', { principal: principal.value, annual_rate: annual_rate.value, months: months.value, elapsed: elapsed.value, persist: persist.value })
  } catch (e) { cmpErr.value = '已过期数须在一到总期数减一之间' }
}
</script>
<template><div class="page"><h1>等额本息试算</h1>
<label>本金 <input v-model.number="principal" /></label>
<label>年利率% <input v-model.number="annual_rate" /></label>
<label>月数 <input v-model.number="months" /></label>
<button @click="run">计算</button>
<p v-if="out">月供 {{ out.monthly_payment }} · 利息合计 {{ out.total_interest }}</p>
<h2>结清与续还对照</h2>
<label>已过期数 <input v-model.number="elapsed" /></label>
<label><input type="checkbox" v-model="persist" /> 保存对照记录</label>
<button @click="compare">对照试算</button>
<p v-if="cmpErr">{{ cmpErr }}</p>
<table v-if="cmp">
<tr><th>已过期数</th><th>期末剩余本金</th><th>续还剩余利息</th><th>结清需还余额</th><th>续还超额利息</th></tr>
<tr><td>{{ cmp.elapsed }}</td><td>{{ cmp.remaining_principal }}</td><td>{{ cmp.remaining_interest }}</td><td>{{ cmp.payoff_amount }}</td><td>{{ cmp.excess_interest }}</td></tr>
</table>
<p v-if="cmp && cmp.run_id">已保存记录 #{{ cmp.run_id }}</p>
</div></template>
