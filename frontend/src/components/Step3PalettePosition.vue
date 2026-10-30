<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { COLOR_PALETTES, COMPOSITION_TYPES } from '../types/voting'
import ApparelMockup from './ApparelMockup.vue'
import {
  ArrowLeft,
  ArrowRight,
  Check,
  CheckCircle2,
  Layers,
  Palette,
} from '@lucide/vue'

const store = useVotingStore()

function handleNext() {
  store.goToStep(4)
}

function handleBack() {
  store.goToStep(2)
}
</script>

<template>
  <div class="max-w-6xl mx-auto py-5 sm:py-8">
    <div class="mb-5 sm:mb-6">
      <h2 class="text-xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
        Elige el Color y la Posición
      </h2>
      <p class="text-xs sm:text-sm text-slate-300 mt-1">
        Selecciona la combinación de colores y cómo te gustaría que se acomode el logotipo.
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 sm:gap-6 items-start">
      <!-- Preview Mockup (Placed first on mobile for immediate visual feedback, sticky right on desktop) -->
      <div class="order-1 lg:order-2 lg:col-span-5 lg:sticky lg:top-24">
        <ApparelMockup />
      </div>

      <!-- Selectors (order-2 on mobile, col-span-7 on desktop) -->
      <div class="order-2 lg:order-1 lg:col-span-7 space-y-5 sm:space-y-6">
        <!-- Palette Picker -->
        <div>
          <div class="flex items-center gap-2 mb-2.5 sm:mb-3 text-xs font-mono uppercase tracking-wider text-slate-200 font-bold">
            <Palette class="w-4 h-4 text-blue-400" />
            <span>Colores</span>
          </div>

          <div class="grid grid-cols-2 gap-2.5 sm:gap-3">
            <div
              v-for="pal in COLOR_PALETTES"
              :key="pal.id"
              :data-cy="'palette-option-' + pal.id"
              @click="store.selectedPalette = pal.id"
              class="solid-card rounded-xl sm:rounded-2xl p-3 sm:p-3.5 cursor-pointer relative transition-all active:scale-[0.98]"
              :class="[
                store.selectedPalette === pal.id
                  ? 'solid-card-active'
                  : ''
              ]"
            >
              <div class="flex items-center justify-between gap-1.5">
                <div class="flex items-center gap-2.5 min-w-0">
                  <div class="flex items-center -space-x-1 shrink-0">
                    <span
                      class="w-5 h-5 rounded-full border-2 border-slate-900 shadow-md"
                      :style="{ backgroundColor: pal.primaryHex }"
                    />
                    <span
                      class="w-5 h-5 rounded-full border-2 border-slate-900 shadow-md"
                      :style="{ backgroundColor: pal.secondaryHex }"
                    />
                  </div>
                  <span class="text-xs sm:text-sm font-bold text-slate-100 truncate">
                    {{ pal.name }}
                  </span>
                </div>

                <div
                  class="w-5 h-5 rounded-full flex items-center justify-center shrink-0 transition-all"
                  :class="[
                    store.selectedPalette === pal.id
                      ? 'bg-blue-600 text-white border-2 border-blue-400 shadow-sm'
                      : 'border-2 border-slate-600 bg-slate-900/80 text-transparent'
                  ]"
                >
                  <Check class="w-3 h-3 stroke-[3]" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Composition Picker -->
        <div>
          <div class="flex items-center gap-2 mb-2.5 sm:mb-3 text-xs font-mono uppercase tracking-wider text-slate-200 font-bold">
            <Layers class="w-4 h-4 text-blue-400" />
            <span>Posición y Formato</span>
          </div>

          <div class="space-y-2 sm:space-y-2.5">
            <div
              v-for="comp in COMPOSITION_TYPES"
              :key="comp.id"
              :data-cy="'comp-option-' + comp.id"
              @click="store.selectedComposition = comp.id"
              class="solid-card rounded-xl sm:rounded-2xl p-3 sm:p-3.5 cursor-pointer relative transition-all active:scale-[0.99]"
              :class="[
                store.selectedComposition === comp.id
                  ? 'solid-card-active'
                  : ''
              ]"
            >
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-xs sm:text-sm font-bold text-slate-100">
                    {{ comp.name }}
                  </h4>
                  <p class="text-[11px] sm:text-xs text-slate-300 mt-0.5">
                    {{ comp.subtitle }}
                  </p>
                </div>

                <div
                  class="w-5 h-5 rounded-full flex items-center justify-center shrink-0 transition-all"
                  :class="[
                    store.selectedComposition === comp.id
                      ? 'bg-blue-600 text-white border-2 border-blue-400 shadow-sm'
                      : 'border-2 border-slate-600 bg-slate-900/80 text-transparent'
                  ]"
                >
                  <CheckCircle2 class="w-3.5 h-3.5 stroke-[2.5]" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div class="flex items-center justify-between mt-6 sm:mt-8 pt-4 sm:pt-6 border-t border-slate-800 gap-3">
      <button
        type="button"
        data-cy="step3-back-btn"
        @click="handleBack"
        class="btn-secondary px-4 sm:px-5 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 sm:gap-2 cursor-pointer shrink-0"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Atrás</span>
      </button>

      <button
        type="button"
        data-cy="step3-next-btn"
        @click="handleNext"
        class="btn-primary px-5 sm:px-6 py-2.5 rounded-xl font-semibold text-xs sm:text-sm flex items-center justify-center gap-1.5 sm:gap-2 cursor-pointer shrink-0"
      >
        <span>Confirmar Voto</span>
        <ArrowRight class="w-4 h-4 stroke-[2]" />
      </button>
    </div>
  </div>
</template>
