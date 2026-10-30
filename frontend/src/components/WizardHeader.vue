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
    <div class="max-w-5xl mx-auto px-3.5 py-2.5 sm:px-6 sm:py-3.5">
      <!-- Header Bar -->
      <div class="flex items-center justify-between gap-2 mb-2.5 sm:mb-3.5">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl bg-blue-600 flex items-center justify-center font-bold text-white text-xs sm:text-base shrink-0">
            ICD
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-1.5 min-w-0">
              <h1 data-cy="header-title" class="text-xs sm:text-base font-bold text-slate-100 tracking-tight leading-tight truncate">
                Votación de Logotipo Oficial
              </h1>
              <span class="bg-blue-950 text-blue-300 border border-blue-500/50 text-[10px] sm:text-xs font-mono px-1.5 py-0.2 rounded font-semibold shrink-0">
                Ronda 1
              </span>
            </div>
            <p class="text-[11px] sm:text-xs text-slate-300 truncate">
              <span class="hidden sm:inline">Ingeniería en Ciencias de Datos · 1 voto por estudiante · Enfoque iterativo</span>
              <span class="sm:hidden">ICD · 1 voto por estudiante · Iterativo</span>
            </p>
          </div>
        </div>

        <div v-if="store.studentCode && store.isCodeValid" data-cy="header-student-badge" class="flex items-center gap-1.5 bg-slate-800/90 border border-slate-700 rounded-lg px-2.5 py-1 text-xs font-mono shrink-0 shadow-sm">
          <span class="text-slate-300 hidden sm:inline">Estudiante:</span>
          <span data-cy="header-student-code" class="font-bold text-blue-400 font-mono tracking-wider">{{ store.studentCode }}</span>
        </div>
      </div>

      <!-- Stepper Navigation -->
      <nav aria-label="Progreso de votación" class="w-full">
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
