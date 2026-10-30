<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { CANDIDATE_FIGURES } from '../types/voting'
import { ArrowLeft, ArrowRight, CheckCircle2 } from '@lucide/vue'

const store = useVotingStore()

function selectFigure(id: string) {
  store.selectedFigure = id
}

function handleNext() {
  store.goToStep(3)
}

function handleBack() {
  store.goToStep(1)
}
</script>

<template>
  <div class="max-w-5xl mx-auto py-5 sm:py-8">
    <div class="text-center mb-5 sm:mb-6">
      <h2 class="text-xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
        Elige la Figura para el Logotipo
      </h2>
      <p class="text-xs sm:text-sm text-slate-300 mt-1">
        Selecciona el símbolo que más te guste para representar a la carrera.
      </p>
    </div>

    <!-- 6 Figures Grid: 2 columns on mobile, 3 columns on desktop -->
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
      <div
        v-for="fig in CANDIDATE_FIGURES"
        :key="fig.id"
        :data-cy="'figure-card-' + fig.id"
        @click="selectFigure(fig.id)"
        class="solid-card rounded-xl sm:rounded-2xl p-3 sm:p-4 cursor-pointer relative flex flex-col justify-between transition-all active:scale-[0.98]"
        :class="[
          store.selectedFigure === fig.id
            ? 'solid-card-active'
            : ''
        ]"
      >
        <div class="flex items-center justify-between mb-2 sm:mb-3">
          <span class="text-[11px] sm:text-xs font-mono bg-slate-800/90 border border-slate-700 text-slate-300 px-2 py-0.5 rounded">
            Opción {{ fig.slot }}
          </span>

          <div
            class="w-5 h-5 rounded-full flex items-center justify-center transition-all"
            :class="[
              store.selectedFigure === fig.id
                ? 'bg-blue-600 text-white border-2 border-blue-400 shadow-sm'
                : 'border-2 border-slate-600 bg-slate-900/80 text-transparent'
            ]"
          >
            <CheckCircle2 class="w-3.5 h-3.5 sm:w-4 sm:h-4 stroke-[2.5]" />
          </div>
        </div>

        <div class="w-full aspect-square max-h-32 sm:max-h-44 rounded-lg sm:rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-center p-3 sm:p-5 mb-2.5 sm:mb-3 shadow-inner">
          <img
            :src="fig.svgPath(store.selectedPalette)"
            :alt="fig.name"
            class="w-full h-full object-contain pointer-events-none select-none"
            loading="lazy"
          />
        </div>

        <div>
          <h3 data-cy="figure-name" class="text-xs sm:text-base font-bold text-slate-100 truncate">
            {{ fig.name }}
          </h3>
          <p class="text-[11px] sm:text-xs text-slate-300 mt-0.5 line-clamp-1 sm:line-clamp-none">
            {{ fig.subtitle }}
          </p>
        </div>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div class="flex items-center justify-between mt-6 sm:mt-8 pt-4 sm:pt-6 border-t border-slate-800 gap-3">
      <button
        type="button"
        data-cy="step2-back-btn"
        @click="handleBack"
        class="btn-secondary px-4 sm:px-5 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 sm:gap-2 cursor-pointer shrink-0"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Atrás</span>
      </button>

      <button
        type="button"
        data-cy="step2-next-btn"
        @click="handleNext"
        class="btn-primary px-4 sm:px-6 py-2.5 rounded-xl font-semibold text-xs sm:text-sm flex items-center justify-center gap-1.5 sm:gap-2 cursor-pointer shrink-0"
      >
        <span class="hidden sm:inline">Siguiente: Color y Posición</span>
        <span class="sm:hidden">Siguiente</span>
        <ArrowRight class="w-4 h-4 stroke-[2]" />
      </button>
    </div>
  </div>
</template>
