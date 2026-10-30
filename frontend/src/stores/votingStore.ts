import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import { z } from 'zod'
import { useVotingApi } from '@/api'
import {
  CANDIDATE_FIGURES,
  COLOR_PALETTES,
  COMPOSITION_TYPES,
  FABRIC_COLORS,
  type StudentVote,
} from '../types/voting'

const StudentCodeSchema = z
  .string()
  .trim()
  .regex(/^\d{8}$/, 'El código debe tener exactamente 8 dígitos numéricos')

export const useVotingStore = defineStore('voting', () => {
  const currentStep = ref<1 | 2 | 3 | 4>(1)
  const studentCode = ref('')
  const codeError = ref<string | null>(null)
  const isValidatingCode = ref(false)
  const submitError = ref<string | null>(null)

  const selectedFigure = ref('c4-tesseract')
  const selectedPalette = ref('emerald')
  const selectedComposition = ref<'symbols' | 'lockups' | 'stacked'>('lockups')
  const selectedFabric = ref<'black' | 'charcoal' | 'gray'>('black')
  const recommendations = ref('')

  const isSubmitting = ref(false)
  const submittedVote = ref<StudentVote | null>(null)
  const showReceiptModal = ref(false)

  const isCodeValid = computed(() => {
    return /^\d{8}$/.test(studentCode.value.trim())
  })

  const activeFigure = computed(() => {
    return CANDIDATE_FIGURES.find((f) => f.id === selectedFigure.value) || CANDIDATE_FIGURES[0]
  })

  const activePalette = computed(() => {
    return COLOR_PALETTES.find((p) => p.id === selectedPalette.value) || COLOR_PALETTES[0]
  })

  const activeComposition = computed(() => {
    return COMPOSITION_TYPES.find((c) => c.id === selectedComposition.value) || COMPOSITION_TYPES[0]
  })

  const activeFabric = computed(() => {
    return FABRIC_COLORS.find((f) => f.id === selectedFabric.value) || FABRIC_COLORS[0]
  })

  const currentAssetUrl = computed(() => {
    const fig = selectedFigure.value
    const comp = selectedComposition.value
    const pal = selectedPalette.value
    const isLight = selectedFabric.value === 'gray'

    let prefix = 'lockup'
    if (comp === 'symbols') {
      prefix = 'symbol'
      return `/candidates/${fig}/${comp}/${prefix}-${pal}.svg`
    }
    if (comp === 'stacked') prefix = 'stacked'

    const variant = isLight ? `${prefix}-${pal}-light.svg` : `${prefix}-${pal}.svg`
    return `/candidates/${fig}/${comp}/${variant}`
  })

  watch(studentCode, (newVal) => {
    const trimmed = newVal.trim()
    codeError.value = null

    if (trimmed.length > 0 && !/^\d+$/.test(trimmed)) {
      codeError.value = 'Solo se permiten dígitos numéricos'
    }
  })

  async function validateAndProceedStep1(): Promise<boolean> {
    const result = StudentCodeSchema.safeParse(studentCode.value)
    if (!result.success) {
      codeError.value = result.error.issues[0]?.message || 'Código inválido'
      return false
    }

    isValidatingCode.value = true
    codeError.value = null

    try {
      const { checkStudent } = useVotingApi()
      const res = await checkStudent({ student_id: studentCode.value.trim() })
      if (res.has_voted) {
        codeError.value = 'Este carné ya ha emitido su voto oficial. Cada estudiante dispone de un único voto.'
        return false
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.message) {
        if (err.message.includes('ya emitió') || err.message.includes('ya tiene')) {
          codeError.value = err.message
          return false
        }
      }
      console.warn('Backend verification notice:', err)
    } finally {
      isValidatingCode.value = false
    }

    currentStep.value = 2
    return true
  }

  function goToStep(step: 1 | 2 | 3 | 4) {
    if (step > 1 && !isCodeValid.value) {
      codeError.value = 'Debes ingresar un código válido de 8 dígitos para continuar'
      currentStep.value = 1
      return
    }
    currentStep.value = step
  }

  async function submitVote(): Promise<boolean> {
    if (!isCodeValid.value) {
      codeError.value = 'Código de estudiante inválido'
      currentStep.value = 1
      return false
    }

    isSubmitting.value = true
    submitError.value = null

    try {
      const { submitVote: apiSubmitVote } = useVotingApi()
      const receipt = await apiSubmitVote({
        student_id: studentCode.value.trim(),
        student_name: `Estudiante ${studentCode.value.trim()}`,
        figure_id: selectedFigure.value as any,
        palette_id: selectedPalette.value as any,
        position_id: selectedComposition.value as any,
        rationale: recommendations.value.trim(),
      })

      const voteRecord: StudentVote = {
        round: `Ronda ${receipt.round}`,
        studentCode: receipt.student_id,
        figureId: receipt.figure_id,
        paletteId: receipt.palette_id,
        compositionId: receipt.position_id as any,
        recommendations: recommendations.value.trim(),
        timestamp: new Date(receipt.timestamp).getTime(),
        isoDate: receipt.timestamp,
      }

      console.log('Voto registrado en el servidor:', receipt)
      submittedVote.value = voteRecord
      showReceiptModal.value = true
      return true
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : 'Error al registrar el voto en el servidor'
      submitError.value = errMsg
      if (errMsg.includes('ya emitió') || errMsg.includes('ya tiene')) {
        codeError.value = 'Este carné ya ha emitido su voto oficial.'
      }
      return false
    } finally {
      isSubmitting.value = false
    }
  }

  function resetForm() {
    studentCode.value = ''
    codeError.value = null
    submitError.value = null
    recommendations.value = ''
    submittedVote.value = null
    showReceiptModal.value = false
    currentStep.value = 1
  }

  return {
    currentStep,
    studentCode,
    codeError,
    isValidatingCode,
    submitError,
    selectedFigure,
    selectedPalette,
    selectedComposition,
    selectedFabric,
    recommendations,
    isSubmitting,
    submittedVote,
    showReceiptModal,
    isCodeValid,
    activeFigure,
    activePalette,
    activeComposition,
    activeFabric,
    currentAssetUrl,
    validateAndProceedStep1,
    goToStep,
    submitVote,
    resetForm,
  }
})
