<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const parse = (h) => { try { return JSON.parse(h.result_json) } catch { return {} } }
onMounted(async () => {
  const raw = (await getJSON('/api/history')).items
  items.value = raw.map(h => ({ ...h, result: parse(h) }))
})
</script>
<template><div class="page"><h1>试算记录</h1>
<table>
<tr><th>#</th><th>类型</th><th>时间</th><th>结果</th></tr>
<tr v-for="h in items" :key="h.id">
<td>#{{ h.id }}</td><td>{{ h.kind }}</td><td>{{ h.created_at }}</td>
<td v-if="h.kind === 'payoff_compare'">第{{ h.result.elapsed }}期 · 剩余本金 {{ h.result.remaining_principal }} · 续还利息 {{ h.result.remaining_interest }} · 结清余额 {{ h.result.payoff_amount }}</td>
<td v-else>月供 {{ h.result.monthly_payment }} · 利息合计 {{ h.result.total_interest }}</td>
</tr>
</table>
</div></template>
