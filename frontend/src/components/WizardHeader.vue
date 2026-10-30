<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { Check } from '@lucide/vue'

const store = useVotingStore()

const steps = [
  { num: 1, label: 'Identificación' },
  { num: 2, label: 'Figura' },
  { num: 3, label: 'Color y Posición' },
  { num: 4, label: 'Confirmación' },
] as const
</script>

<template>
  <header class="w-full border-b border-slate-800 bg-slate-900/95 sticky top-0 z-30">
    <div class="max-w-5xl mx-auto px-3.5 py-2.5 sm:px-6 sm:py-3">
      <!-- Stepper Navigation -->
      <nav aria-label="Progreso de votación" data-cy="stepper-nav" class="w-full">
        <ol class="grid grid-cols-4 gap-1.5 sm:gap-2">
          <li
            v-for="s in steps"
            :key="s.num"
            class="relative flex flex-col"
          >
            <button
              type="button"
              :data-cy="'step-indicator-' + s.num"
              :disabled="s.num > store.currentStep && !store.isCodeValid"
              @click="store.goToStep(s.num)"
              class="flex items-center justify-center sm:justify-start gap-1.5 sm:gap-2 text-left py-0.5 sm:py-1 transition-all focus:outline-none"
              :class="[
                s.num === store.currentStep ? 'cursor-default' : '',
                s.num < store.currentStep ? 'cursor-pointer hover:opacity-90' : '',
                s.num > store.currentStep ? 'opacity-40 cursor-not-allowed' : ''
              ]"
            >
              <span
                class="w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center font-mono text-[11px] sm:text-xs font-bold shrink-0 transition-all"
                :class="[
                  s.num === store.currentStep
                    ? 'bg-blue-600 text-white ring-2 ring-blue-500/50 shadow-sm'
                    : s.num < store.currentStep
                    ? 'bg-blue-950 text-blue-300 border border-blue-500/80 font-bold'
                    : 'bg-slate-800 text-slate-400 border border-slate-700'
                ]"
              >
                <Check v-if="s.num < store.currentStep" class="w-3 h-3 sm:w-3.5 sm:h-3.5 stroke-[3]" />
                <span v-else>{{ s.num }}</span>
              </span>

              <span
                class="hidden md:inline text-xs font-medium truncate"
                :class="s.num === store.currentStep ? 'text-blue-400 font-semibold' : s.num < store.currentStep ? 'text-slate-200' : 'text-slate-400'"
              >
                {{ s.label }}
              </span>
            </button>

            <div
              class="w-full rounded-full mt-1 sm:mt-1.5 transition-all"
              :class="[
                s.num === store.currentStep
                  ? 'bg-blue-500 h-1'
                  : s.num < store.currentStep
                  ? 'bg-blue-700 h-0.5 sm:h-1'
                  : 'bg-slate-800 h-0.5'
              ]"
            />
          </li>
        </ol>
      </nav>
    </div>
  </header>
</template>
