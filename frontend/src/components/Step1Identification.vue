<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { AlertCircle, ArrowRight, Fingerprint, Info, Loader2 } from '@lucide/vue'

const store = useVotingStore()

async function handleContinue() {
  await store.validateAndProceedStep1()
}
</script>

<template>
  <div class="max-w-xl mx-auto py-5 sm:py-12">
    <div class="solid-panel rounded-2xl p-5 sm:p-9 shadow-lg">
      <div class="text-center mb-5 sm:mb-6">
        <h2 class="text-xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
          Elige el Logotipo de tu Carrera
        </h2>
        <p class="text-xs sm:text-sm text-slate-300 mt-1.5 sm:mt-2">
          Ingresa tu código de estudiante para comenzar y seleccionar tu opción favorita.
        </p>
      </div>

      <!-- Information Card: 1 Vote Rule -->
      <div class="mb-5 sm:mb-6 p-3.5 sm:p-4 rounded-xl bg-slate-950/90 border border-slate-800 text-left space-y-2 text-xs">
        <div class="flex items-center gap-2 font-bold text-slate-200">
          <Info class="w-4 h-4 text-blue-400 shrink-0" />
          <span>Condiciones de Participación</span>
        </div>
        <div class="space-y-1.5 text-slate-300 leading-relaxed font-sans">
          <p class="flex items-start gap-1.5">
            <span class="text-blue-400 font-bold">•</span>
            <span><strong class="text-white">1 voto por estudiante:</strong> Tu código oficial solo permite emitir un único voto intransferible.</span>
          </p>
        </div>
      </div>

      <form @submit.prevent="handleContinue" class="space-y-5 sm:space-y-6">
        <div>
          <label for="studentCode" class="block text-xs font-mono uppercase tracking-wider text-slate-200 font-bold mb-2">
            Código de Estudiante
          </label>

          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <Fingerprint class="w-5 h-5 text-blue-400" />
            </div>

            <input
              id="studentCode"
              data-cy="student-code-input"
              v-model="store.studentCode"
              type="text"
              inputmode="numeric"
              pattern="[0-9]*"
              maxlength="8"
              placeholder="Ej: 21948573"
              class="w-full pl-11 pr-24 py-3.5 bg-slate-950 border rounded-xl font-mono text-base sm:text-lg tracking-wider text-slate-100 placeholder:text-slate-500 focus:outline-none transition-all"
              :class="[
                store.codeError
                  ? 'border-rose-500 ring-2 ring-rose-500/20'
                  : store.isCodeValid
                  ? 'border-emerald-500 ring-2 ring-emerald-500/20'
                  : 'border-slate-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30'
              ]"
            />

            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <span
                data-cy="student-code-counter"
                class="text-xs font-mono px-2 py-0.5 rounded transition-all"
                :class="store.studentCode.length === 8 ? 'text-emerald-300 font-bold bg-emerald-950/80 border border-emerald-600/60 shadow-sm' : 'text-slate-400 bg-slate-800/80 border border-slate-700/60'"
              >
                {{ store.studentCode.length }} / 8
              </span>
            </div>
          </div>

          <!-- Error Feedback -->
          <div v-if="store.codeError" data-cy="student-code-error" class="mt-2.5 p-2.5 rounded-xl bg-rose-950/40 border border-rose-800/60 flex items-start gap-2 text-xs font-mono text-rose-300">
            <AlertCircle class="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
            <span>{{ store.codeError }}</span>
          </div>
        </div>

        <button
          type="submit"
          data-cy="step1-continue-btn"
          :disabled="!store.isCodeValid || store.isValidatingCode"
          class="w-full btn-primary min-h-[48px] py-3.5 rounded-xl font-semibold text-sm sm:text-base flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="store.isValidatingCode" class="flex items-center gap-2">
            <Loader2 class="w-4 h-4 animate-spin" />
            <span>Verificando carné...</span>
          </span>
          <span v-else class="flex items-center gap-2">
            <span>Continuar</span>
            <ArrowRight class="w-4 h-4 stroke-[2]" />
          </span>
        </button>
      </form>
    </div>
  </div>
</template>
