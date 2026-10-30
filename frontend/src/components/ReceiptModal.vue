<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { CheckCircle2, RotateCcw, X } from '@lucide/vue'

const store = useVotingStore()

function handleClose() {
  store.showReceiptModal = false
}

function handleReset() {
  store.resetForm()
}
</script>

<template>
  <div
    v-if="store.showReceiptModal && store.submittedVote"
    class="fixed inset-0 z-50 flex items-center justify-center p-3.5 sm:p-4 bg-black/85 backdrop-blur-sm"
  >
    <div
      data-cy="receipt-modal"
      class="solid-panel w-full max-w-md rounded-2xl sm:rounded-3xl p-5 sm:p-7 border border-slate-700 shadow-2xl relative overflow-hidden"
    >
      <!-- Top Accent Bar -->
      <div class="h-1.5 w-full bg-blue-600 absolute top-0 left-0 right-0" />

      <button
        type="button"
        data-cy="receipt-close-btn"
        @click="handleClose"
        class="absolute top-4 right-4 p-1.5 rounded-full text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
      >
        <X class="w-5 h-5" />
      </button>

      <div class="flex items-center gap-3 sm:gap-3.5 mb-3.5 sm:mb-4 pt-1">
        <div class="w-10 h-10 sm:w-11 sm:h-11 rounded-xl sm:rounded-2xl bg-blue-950 border border-blue-500/60 flex items-center justify-center text-blue-400 shrink-0 shadow-sm">
          <CheckCircle2 class="w-5 h-5 sm:w-6 sm:h-6 stroke-[2.5]" />
        </div>
        <div>
          <h3 class="text-lg sm:text-xl font-bold text-slate-100 tracking-tight">
            ¡Voto Registrado!
          </h3>
          <p class="text-xs text-slate-300">
            Confirmación oficial de participación electoral ICD.
          </p>
        </div>
      </div>

      <!-- Summary -->
      <div class="bg-slate-950 rounded-xl sm:rounded-2xl p-4 border border-slate-800 space-y-2.5 font-mono text-xs my-4 sm:my-5 shadow-inner">
        <div class="flex items-center justify-between pb-2 border-b border-slate-800">
          <span class="text-slate-300 font-semibold">ESTUDIANTE:</span>
          <span data-cy="receipt-student-code" class="text-blue-400 font-bold tracking-wider">{{ store.submittedVote.studentCode }}</span>
        </div>
        <div class="flex items-center justify-between pb-2 border-b border-slate-800 gap-2">
          <span class="text-slate-300 font-semibold shrink-0">FIGURA:</span>
          <span data-cy="receipt-figure" class="text-white font-bold truncate">{{ store.activeFigure.name }}</span>
        </div>
        <div class="flex items-center justify-between pb-2 border-b border-slate-800 gap-2">
          <span class="text-slate-300 font-semibold shrink-0">COLOR:</span>
          <span data-cy="receipt-palette" class="text-white font-bold truncate">{{ store.activePalette.name }}</span>
        </div>
        <div class="flex items-center justify-between pb-2 border-b border-slate-800 gap-2">
          <span class="text-slate-300 font-semibold shrink-0">POSICIÓN:</span>
          <span data-cy="receipt-composition" class="text-white font-bold truncate">{{ store.activeComposition.name }}</span>
        </div>
        <div v-if="store.submittedVote.hasAttachment" class="flex items-center justify-between pb-2 border-b border-slate-800 gap-2">
          <span class="text-slate-300 font-semibold shrink-0">ADJUNTO:</span>
          <span data-cy="receipt-attachment" class="text-emerald-400 font-bold truncate">
            ✓ {{ store.submittedVote.attachmentFilename || 'Propuesta recibida' }}
          </span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-slate-300 font-semibold">FECHA:</span>
          <span class="text-slate-300 text-[11px]">{{ new Date(store.submittedVote.timestamp).toLocaleDateString('es-MX') }}</span>
        </div>
      </div>

      <!-- Confirmation Note -->
      <p class="text-[11px] text-slate-300 text-center mb-4 leading-relaxed font-sans">
        Tu voto único ha sido registrado exitosamente en el sistema oficial de la carrera.
      </p>

      <!-- Action Buttons -->
      <div class="flex items-center justify-center">
        <button
          type="button"
          data-cy="finish-vote-btn"
          @click="handleReset"
          class="w-full btn-primary min-h-[44px] py-2.5 sm:py-3 px-6 rounded-xl text-xs sm:text-sm font-bold flex items-center justify-center gap-2 cursor-pointer active:scale-[0.99] shadow-sm"
        >
          <RotateCcw class="w-4 h-4" />
          <span>Finalizar</span>
        </button>
      </div>
    </div>
  </div>
</template>
