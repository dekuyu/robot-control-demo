// ===== 变量读写 Store =====
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { VariableData, IOSignal } from '@/types/variable'
import { variableAPI } from '@/api/variable'

export const useVariableStore = defineStore('variable', () => {
  const bVariables = ref<Map<number, number>>(new Map())
  const iVariables = ref<Map<number, number>>(new Map())
  const dVariables = ref<Map<number, number>>(new Map())
  const ioSignals = ref<Map<number, number>>(new Map())
  const loading = ref(false)
  const selectedVarType = ref<'B' | 'I' | 'D' | 'IO'>('B')

  async function readB(index: number) {
    const res = await variableAPI.readB(index)
    if (res.data) bVariables.value.set(index, res.data.value as number)
    return res
  }

  async function writeB(index: number, value: number) {
    const res = await variableAPI.writeB(index, value)
    if (res.code === 0) bVariables.value.set(index, value)
    return res
  }

  async function batchReadB(indices: number[]) {
    loading.value = true
    try {
      const res = await variableAPI.batchReadB(indices)
      if (res.data?.values) {
        for (const v of res.data.values) {
          bVariables.value.set(v.index, v.value as number)
        }
      }
    } finally {
      loading.value = false
    }
  }

  async function readI(index: number) {
    const res = await variableAPI.readI(index)
    if (res.data) iVariables.value.set(index, res.data.value as number)
    return res
  }

  async function readD(index: number) {
    const res = await variableAPI.readD(index)
    if (res.data) dVariables.value.set(index, res.data.value as number)
    return res
  }

  async function writeD(index: number, value: number) {
    const res = await variableAPI.writeD(index, value)
    if (res.code === 0) dVariables.value.set(index, value)
    return res
  }

  async function readIO(index: number) {
    const res = await variableAPI.readIO(index)
    if (res.data) ioSignals.value.set(index, res.data.value)
    return res
  }

  async function writeIO(index: number, value: number) {
    const res = await variableAPI.writeIO(index, value)
    if (res.code === 0) ioSignals.value.set(index, value)
    return res
  }

  function getBValue(index: number): number | undefined { return bVariables.value.get(index) }
  function getIValue(index: number): number | undefined { return iVariables.value.get(index) }
  function getDValue(index: number): number | undefined { return dVariables.value.get(index) }
  function getIOValue(index: number): number | undefined { return ioSignals.value.get(index) }

  return {
    bVariables, iVariables, dVariables, ioSignals, loading, selectedVarType,
    readB, writeB, batchReadB,
    readI, readD, writeD,
    readIO, writeIO,
    getBValue, getIValue, getDValue, getIOValue,
  }
})
