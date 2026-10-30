<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { ArrowLeft, MessageSquare, Send, ShieldAlert, AlertCircle } from '@lucide/vue'

const store = useVotingStore()

async function handleSubmit() {
  await store.submitVote()
}

function handleBack() {
  store.goToStep(3)
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-5 sm:py-10 pb-8">
    <div class="text-center mb-5 sm:mb-6">
      <h2 class="text-xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
        Confirma tu Selección
      </h2>
      <p class="text-xs sm:text-sm text-slate-300 mt-1">
        Revisa las opciones que elegiste antes de registrar tu voto.
      </p>
    </div>

    <!-- Ballot Summary Card -->
    <div class="solid-panel rounded-2xl sm:rounded-3xl p-4 sm:p-8 mb-5 sm:mb-6 border border-slate-800 shadow-xl space-y-4 sm:space-y-5">
      <!-- Student Code -->
      <div class="flex items-center justify-between pb-3 sm:pb-4 border-b border-slate-800">
        <span class="text-xs font-mono text-slate-300 uppercase tracking-wider font-semibold">
          Código de Estudiante
        </span>
        <span data-cy="summary-student-code" class="text-base sm:text-lg font-mono font-bold text-blue-400 tracking-wider">
          {{ store.studentCode }}
        </span>
      </div>

      <!-- Choices Summary Rows -->
      <div class="space-y-2.5 sm:space-y-3 font-mono text-xs">
        <div class="flex items-center justify-between p-2.5 sm:p-3 rounded-xl bg-slate-900/90 border border-slate-800 gap-2">
          <div class="flex items-center gap-2 sm:gap-3 min-w-0">
            <span class="text-slate-300 shrink-0 font-medium">Figura:</span>
            <span data-cy="summary-figure-name" class="text-white font-bold truncate">{{ store.activeFigure.name }}</span>
          </div>
          <button
            type="button"
            data-cy="change-figure-btn"
            @click="store.goToStep(2)"
            class="btn-secondary text-xs px-2.5 py-1 rounded-lg shrink-0 font-mono active:scale-95 transition-all"
          >
            Cambiar
          </button>
        </div>

        <div class="flex items-center justify-between p-2.5 sm:p-3 rounded-xl bg-slate-900/90 border border-slate-800 gap-2">
          <div class="flex items-center gap-2 sm:gap-3 min-w-0">
            <span class="text-slate-300 shrink-0 font-medium">Color:</span>
            <span data-cy="summary-palette-name" class="text-white font-bold truncate">{{ store.activePalette.name }}</span>
          </div>
          <button
            type="button"
            data-cy="change-palette-btn"
            @click="store.goToStep(3)"
            class="btn-secondary text-xs px-2.5 py-1 rounded-lg shrink-0 font-mono active:scale-95 transition-all"
          >
            Cambiar
          </button>
        </div>

        <div class="flex items-center justify-between p-2.5 sm:p-3 rounded-xl bg-slate-900/90 border border-slate-800 gap-2">
          <div class="flex items-center gap-2 sm:gap-3 min-w-0">
            <span class="text-slate-300 shrink-0 font-medium">Posición:</span>
            <span data-cy="summary-composition-name" class="text-white font-bold truncate">{{ store.activeComposition.name }}</span>
          </div>
          <button
            type="button"
            data-cy="change-composition-btn"
            @click="store.goToStep(3)"
            class="btn-secondary text-xs px-2.5 py-1 rounded-lg shrink-0 font-mono active:scale-95 transition-all"
          >
            Cambiar
          </button>
        </div>
      </div>

      <!-- Live Vector Preview Box -->
      <div class="w-full aspect-video max-h-36 sm:max-h-44 rounded-xl sm:rounded-2xl bg-slate-950 border border-slate-800/80 flex items-center justify-center p-3 sm:p-4 shadow-inner">
        <img
          data-cy="summary-preview-img"
          :src="store.currentAssetUrl"
          :alt="store.activeFigure.name"
          class="max-h-24 sm:max-h-32 max-w-full object-contain filter drop-shadow-md"
        />
      </div>

      <!-- Textarea for Student Recommendations -->
      <div class="pt-1 sm:pt-2">
        <label for="recommendations" class="block text-xs font-mono uppercase tracking-wider text-slate-200 font-semibold mb-2 flex items-center gap-1.5">
          <MessageSquare class="w-3.5 h-3.5 text-blue-400" />
          <span>Comentarios o sugerencias (Opcional)</span>
        </label>
        <textarea
          id="recommendations"
          data-cy="recommendations-textarea"
          v-model="store.recommendations"
          rows="3"
          placeholder="Escribe alguna sugerencia o comentario..."
          class="w-full px-3.5 sm:px-4 py-2.5 sm:py-3 bg-slate-950 border border-slate-700 rounded-xl text-base sm:text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all font-sans"
        />
      </div>

      <!-- Single Vote Notice -->
      <div class="p-3.5 rounded-xl bg-blue-950/40 border border-blue-500/30 text-xs text-slate-300 space-y-1">
        <div class="flex items-center gap-1.5 font-bold text-blue-300">
          <ShieldAlert class="w-4 h-4 text-blue-400 shrink-0" />
          <span>Voto Único e Intransferible</span>
        </div>
        <p class="text-[11px] sm:text-xs text-slate-300 leading-relaxed font-sans">
          Cada estudiante dispone de <strong>un solo voto</strong>. Una vez enviado, se emitirá tu comprobante digital y tu elección quedará registrada de forma oficial.
        </p>
      </div>

      <!-- Submission Error Feedback -->
      <div
        v-if="store.submitError"
        data-cy="submit-error-banner"
        class="p-3.5 rounded-xl bg-rose-950/60 border border-rose-800 text-xs font-mono text-rose-300 flex items-start gap-2.5"
      >
        <AlertCircle class="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
        <div class="space-y-1">
          <p class="font-bold text-rose-200">No se pudo emitir el voto</p>
          <p>{{ store.submitError }}</p>
        </div>
      </div>
    </div>

    <!-- Actions: Full-width stacked on mobile for thumb accessibility, row on desktop -->
    <div class="flex flex-col-reverse sm:flex-row items-stretch sm:items-center justify-between gap-3">
      <button
        type="button"
        data-cy="step4-back-btn"
        @click="handleBack"
        class="btn-secondary min-h-[44px] px-5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-center gap-2 cursor-pointer"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Atrás</span>
      </button>

      <button
        type="button"
        data-cy="submit-vote-btn"
        :disabled="store.isSubmitting"
        @click="handleSubmit"
        class="btn-primary min-h-[48px] px-7 py-3 rounded-xl font-bold text-sm tracking-wide flex items-center justify-center gap-2 cursor-pointer shadow-md active:scale-[0.99]"
      >
        <Send class="w-4 h-4 stroke-[2.5]" />
        <span>{{ store.isSubmitting ? 'Enviando...' : 'Enviar Mi Voto' }}</span>
      </button>
    </div>
  </div>
</template>
