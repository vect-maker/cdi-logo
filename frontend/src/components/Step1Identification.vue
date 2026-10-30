<script setup lang="ts">
import { useVotingStore } from '../stores/votingStore'
import { AlertCircle, ArrowRight, Fingerprint } from '@lucide/vue'

const store = useVotingStore()

function handleContinue() {
  store.validateAndProceedStep1()
}
</script>

<template>
  <div class="max-w-xl mx-auto py-6 sm:py-16">
    <div class="solid-panel rounded-2xl p-5 sm:p-10 shadow-lg">
      <div class="text-center mb-6 sm:mb-8">
        <h2 class="text-xl sm:text-3xl font-bold text-slate-100 tracking-tight">
          Elige el Logotipo de tu Carrera
        </h2>
        <p class="text-xs sm:text-sm text-slate-400 mt-1.5 sm:mt-2">
          Ingresa tu código de estudiante para comenzar y seleccionar tu opción favorita.
        </p>
      </div>

      <form @submit.prevent="handleContinue" class="space-y-5 sm:space-y-6">
        <div>
          <label for="studentCode" class="block text-xs font-mono uppercase tracking-wider text-slate-300 font-semibold mb-2">
            Código de Estudiante
          </label>

          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <Fingerprint class="w-5 h-5 text-blue-400" />
            </div>

            <input
              id="studentCode"
              v-model="store.studentCode"
              type="text"
              inputmode="numeric"
              pattern="[0-9]*"
              maxlength="9"
              placeholder="Ej: 219485732"
              class="w-full pl-11 pr-20 py-3.5 bg-slate-900 border rounded-xl font-mono text-base sm:text-lg tracking-wider text-slate-100 placeholder:text-slate-600 focus:outline-none transition-colors"
              :class="[
                store.codeError
                  ? 'border-rose-500 focus:border-rose-500'
                  : store.isCodeValid
                  ? 'border-emerald-500 focus:border-emerald-500'
                  : 'border-slate-700 focus:border-blue-500'
              ]"
            />

            <div class="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none">
              <span
                class="text-xs font-mono"
                :class="store.studentCode.length === 9 ? 'text-emerald-400 font-bold' : 'text-slate-500'"
              >
                {{ store.studentCode.length }} / 9
              </span>
            </div>
          </div>

          <!-- Error Feedback -->
          <div v-if="store.codeError" class="mt-2.5 flex items-start gap-2 text-xs font-mono text-rose-400">
            <AlertCircle class="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
            <span>{{ store.codeError }}</span>
          </div>
        </div>

        <button
          type="submit"
          :disabled="!store.isCodeValid"
          class="w-full btn-primary min-h-[48px] py-3.5 rounded-xl font-semibold text-sm sm:text-base flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-[0.99]"
        >
          <span>Continuar</span>
          <ArrowRight class="w-4 h-4 stroke-[2]" />
        </button>
      </form>
    </div>
  </div>
</template>
