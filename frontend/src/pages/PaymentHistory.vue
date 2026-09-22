<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const parse = (s) => { try { return JSON.parse(s) } catch { return null } }
onMounted(async () => {
  const rows = (await getJSON('/api/history')).items
  items.value = rows.map(r => ({ ...r, input: parse(r.input_json), result: parse(r.result_json) }))
})
</script>
<template><div class="page"><h1>试算记录</h1>
<table>
  <tr><th>#</th><th>类型</th><th>时间</th><th>钉选参数 / 金额</th></tr>
  <tr v-for="h in items" :key="h.id">
    <td>#{{ h.id }}</td>
    <td>{{ h.kind }}</td>
    <td>{{ h.created_at }}</td>
    <td>
      <template v-if="h.kind === 'settle_compare' && h.result">
        第 {{ h.input?.paid_periods }} 期末结清对照 ·
        剩余本金 {{ h.result.remaining_principal }} ·
        续还利息 {{ h.result.remaining_interest }} ·
        结清余额 {{ h.result.settle_amount }} ·
        超额利息 {{ h.result.extra_interest }}
      </template>
      <template v-else-if="h.result">月供 {{ h.result.monthly_payment }} · 利息合计 {{ h.result.total_interest }}</template>
    </td>
  </tr>
</table>
</div></template>
