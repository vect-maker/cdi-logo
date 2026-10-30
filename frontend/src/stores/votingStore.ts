import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import { z } from 'zod'
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

  function validateAndProceedStep1(): boolean {
    const result = StudentCodeSchema.safeParse(studentCode.value)
    if (!result.success) {
      codeError.value = result.error.issues[0]?.message || 'Código inválido'
      return false
    }

    codeError.value = null
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

  function submitVote(): boolean {
    if (!isCodeValid.value) {
      codeError.value = 'Código de estudiante inválido'
      currentStep.value = 1
      return false
    }

    isSubmitting.value = true
    const now = new Date()
    const voteRecord: StudentVote = {
      round: 'Ronda 1',
      studentCode: studentCode.value.trim(),
      figureId: selectedFigure.value,
      paletteId: selectedPalette.value,
      compositionId: selectedComposition.value,
      recommendations: recommendations.value.trim(),
      timestamp: now.getTime(),
      isoDate: now.toISOString(),
    }

    // Print selected data to console
    console.log('Voto emitido:', voteRecord)

    submittedVote.value = voteRecord
    showReceiptModal.value = true
    isSubmitting.value = false
    return true
  }

  function resetForm() {
    studentCode.value = ''
    codeError.value = null
    recommendations.value = ''
    submittedVote.value = null
    showReceiptModal.value = false
    currentStep.value = 1
  }

  return {
    currentStep,
    studentCode,
    codeError,
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
