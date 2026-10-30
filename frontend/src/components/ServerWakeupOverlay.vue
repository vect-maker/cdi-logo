<script setup lang="ts">
import { AlertTriangle, Loader2, RefreshCw, Server } from '@lucide/vue'
import type { ServerWakeupStatus } from '../composables/useServerWakeup'

defineProps<{
  status: ServerWakeupStatus
  elapsedSeconds: number
  attempts: number
}>()

const emit = defineEmits<{
  (e: 'retry'): void
}>()
</script>

<template>
  <div
    data-cy="server-wakeup-overlay"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#0b1120] text-slate-100"
  >
    <div
      class="solid-panel w-full max-w-lg rounded-2xl sm:rounded-3xl p-6 sm:p-9 border border-slate-800 shadow-2xl text-center space-y-6 relative overflow-hidden transition-all duration-300"
    >
      <!-- Top Accent Bar -->
      <div
        class="h-1.5 w-full absolute top-0 left-0 right-0 transition-all duration-500"
        :class="status === 'timeout' ? 'bg-amber-500' : 'bg-blue-600'"
      />

      <!-- Icon Container -->
      <div class="flex justify-center pt-2">
        <!-- Checking / Waking Up State -->
        <div
          v-if="status === 'checking' || status === 'waking_up'"
          class="relative w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-blue-950/80 border border-blue-500/40 flex items-center justify-center text-blue-400 shadow-lg"
        >
          <Server class="w-8 h-8 sm:w-10 sm:h-10 text-blue-400 animate-pulse" />
          <Loader2
            class="absolute -top-1.5 -right-1.5 w-6 h-6 sm:w-7 sm:h-7 text-blue-400 animate-spin stroke-[2.5]"
          />
        </div>

        <!-- Timeout State -->
        <div
          v-else-if="status === 'timeout'"
          data-cy="server-timeout-icon"
          class="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-amber-950/80 border border-amber-500/40 flex items-center justify-center text-amber-400 shadow-lg"
        >
          <AlertTriangle class="w-8 h-8 sm:w-10 sm:h-10 stroke-[2.2]" />
        </div>
      </div>

      <!-- Informative Text -->
      <div class="space-y-2">
        <h2
          data-cy="server-status-title"
          class="text-xl sm:text-2xl font-bold tracking-tight text-white"
        >
          {{
            status === 'checking'
              ? 'Verificando Servidor...'
              : status === 'waking_up'
              ? 'Iniciando Servidor Seguro'
              : 'No se pudo conectar con el servidor'
          }}
        </h2>

        <p
          data-cy="server-status-desc"
          class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-md mx-auto font-sans"
        >
          <span v-if="status === 'checking'">
            Comprobando la disponibilidad del sistema de votación oficial...
          </span>
          <span v-else-if="status === 'waking_up'">
            El servidor se encuentra reactivándose tras un periodo de inactividad. Esto puede tomar
            entre 20 y 45 segundos en el servicio gratuito. Gracias por tu paciencia.
          </span>
          <span v-else-if="status === 'timeout'">
            El servidor tardó más de lo esperado en responder. Por favor verifica tu conexión a internet
            o reintenta iniciar la sesión.
          </span>
        </p>
      </div>

      <!-- Live Counter during Wakeup -->
      <div
        v-if="status === 'waking_up'"
        data-cy="server-wakeup-counter"
        class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-700 font-mono text-xs text-blue-300 shadow-inner"
      >
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
        <span>Tiempo transcurrido: <strong>{{ elapsedSeconds }}s</strong> (intento {{ attempts }})</span>
      </div>

      <!-- Retry Action Button on Timeout -->
      <div v-if="status === 'timeout'" class="pt-2">
        <button
          type="button"
          data-cy="retry-connection-btn"
          @click="emit('retry')"
          class="w-full sm:w-auto btn-primary min-h-[44px] px-6 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center justify-center gap-2 mx-auto cursor-pointer shadow-md active:scale-95 transition-all"
        >
          <RefreshCw class="w-4 h-4 stroke-[2.5]" />
          <span>Reintentar Conexión</span>
        </button>
      </div>
    </div>
  </div>
</template>
