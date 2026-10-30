<script setup lang="ts">
import { computed } from 'vue'
import { useVotingStore } from '../stores/votingStore'
import { FABRIC_COLORS } from '../types/voting'

const store = useVotingStore()

const currentFabric = computed(() => {
  return FABRIC_COLORS.find((f) => f.id === store.selectedFabric) || FABRIC_COLORS[0]
})

const logoContainerClasses = computed(() => {
  switch (store.selectedComposition) {
    case 'symbols':
      return 'w-28 h-28 sm:w-44 sm:h-44'
    case 'lockups':
      return 'w-full max-w-[280px] sm:max-w-[400px] h-auto'
    case 'stacked':
      return 'w-36 sm:w-52 h-auto'
    default:
      return 'w-36 sm:w-52 h-auto'
  }
})
</script>

<template>
  <div class="solid-panel rounded-xl sm:rounded-2xl p-3 sm:p-5 flex flex-col items-center">
    <!-- Top Header Bar with Background Color Selector -->
    <div class="w-full flex items-center justify-between gap-2 mb-2.5 sm:mb-4 pb-2.5 sm:pb-3 border-b border-slate-800">
      <span class="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
        Vista previa en tela
      </span>

      <!-- Color Swatch Buttons -->
      <div class="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
        <span class="text-[11px] font-mono text-slate-400 px-1 hidden sm:inline">Color:</span>
        <button
          v-for="fabric in FABRIC_COLORS"
          :key="fabric.id"
          :data-cy="'fabric-btn-' + fabric.id"
          type="button"
          @click="store.selectedFabric = fabric.id"
          class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono font-medium transition-all"
          :class="[
            store.selectedFabric === fabric.id
              ? 'bg-blue-950/90 text-blue-300 border border-blue-500 shadow-sm ring-1 ring-blue-500/40'
              : 'text-slate-300 hover:text-white hover:bg-slate-800/80 border border-transparent'
          ]"
        >
          <span
            class="w-3.5 h-3.5 rounded-full border border-slate-500 shrink-0 shadow-inner"
            :style="{ backgroundColor: fabric.hex }"
          />
          <span>{{ fabric.name }}</span>
        </button>
      </div>
    </div>

    <!-- Clean Background Canvas Preview -->
    <div
      data-cy="preview-canvas"
      class="relative w-full aspect-[16/10] sm:aspect-[4/3] rounded-xl flex items-center justify-center p-4 sm:p-8 transition-colors duration-150 overflow-hidden border border-slate-700/80 shadow-inner"
      :style="{ backgroundColor: currentFabric.hex }"
    >
      <!-- Centered Logo Display -->
      <div
        class="flex items-center justify-center transition-all duration-200"
        :class="logoContainerClasses"
      >
        <img
          :key="store.currentAssetUrl"
          data-cy="preview-logo-img"
          :src="store.currentAssetUrl"
          :alt="store.activeFigure.name"
          class="w-full h-full object-contain pointer-events-none select-none drop-shadow-sm"
          loading="eager"
        />
      </div>
    </div>
  </div>
</template>
