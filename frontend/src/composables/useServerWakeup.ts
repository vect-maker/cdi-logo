import { ref, onMounted, onUnmounted } from 'vue'
import { useHealthApi } from '../api'

export type ServerWakeupStatus = 'checking' | 'waking_up' | 'ready' | 'timeout'

function getIsCypress(): boolean {
  if (typeof window === 'undefined') return false
  try {
    if ((window as unknown as { Cypress?: unknown }).Cypress) return true
    if (window.parent && (window.parent as unknown as { Cypress?: unknown }).Cypress) return true
    if (window.top && (window.top as unknown as { Cypress?: unknown }).Cypress) return true
  } catch {
    // Cross-origin protection
  }
  return false
}

export function useServerWakeup(options?: {
  timeoutMs?: number
  intervalMs?: number
  graceDelayMs?: number
}) {
  const searchParams = typeof window !== 'undefined' ? new URLSearchParams(window.location.search) : null
  const queryTimeout = searchParams?.get('serverTimeoutMs') ? Number(searchParams.get('serverTimeoutMs')) : null
  const queryInterval = searchParams?.get('serverIntervalMs') ? Number(searchParams.get('serverIntervalMs')) : null
  const queryGrace = searchParams?.get('serverGraceDelayMs') ? Number(searchParams.get('serverGraceDelayMs')) : null

  const isCypress = getIsCypress()
  const timeoutMs = options?.timeoutMs ?? queryTimeout ?? (isCypress ? 2500 : 60000)
  const intervalMs = options?.intervalMs ?? queryInterval ?? (isCypress ? 300 : 2500)
  // Grace delay before rendering full-screen overlay (prevents flash if server is already awake)
  const graceDelayMs = options?.graceDelayMs ?? queryGrace ?? (isCypress ? 150 : 500)

  const status = ref<ServerWakeupStatus>('checking')
  const isOverlayVisible = ref(false)
  const elapsedSeconds = ref(0)
  const attempts = ref(0)
  const lastError = ref<string | null>(null)

  let pollTimer: ReturnType<typeof setTimeout> | null = null
  let clockTimer: ReturnType<typeof setInterval> | null = null
  let graceTimer: ReturnType<typeof setTimeout> | null = null
  let startTime = 0
  let isMounted = true

  const { getHealth } = useHealthApi()

  async function pingHealth(): Promise<boolean> {
    try {
      const res = await getHealth()
      if (res && res.status === 'ok') {
        return true
      }
      return false
    } catch (err: unknown) {
      lastError.value = err instanceof Error ? err.message : 'Error de conexión'
      return false
    }
  }

  async function checkLoop() {
    if (!isMounted || status.value === 'ready' || status.value === 'timeout') {
      return
    }

    attempts.value++
    const isHealthy = await pingHealth()

    if (!isMounted) return

    if (isHealthy) {
      status.value = 'ready'
      isOverlayVisible.value = false
      stopTimers()
      return
    }

    // Health check failed or container is sleeping: show overlay immediately
    isOverlayVisible.value = true

    // Still not ready; calculate elapsed time
    const now = Date.now()
    const elapsed = now - startTime

    if (elapsed >= timeoutMs) {
      status.value = 'timeout'
      stopTimers()
      return
    }

    // Switch to waking_up state if first check didn't succeed
    status.value = 'waking_up'
    pollTimer = setTimeout(checkLoop, intervalMs)
  }

  function start(keepOverlayVisible = false) {
    stopTimers()
    status.value = 'checking'
    isOverlayVisible.value = keepOverlayVisible
    elapsedSeconds.value = 0
    attempts.value = 0
    lastError.value = null
    startTime = Date.now()

    // If server takes longer than graceDelayMs to respond to initial check, show the overlay
    if (!keepOverlayVisible) {
      graceTimer = setTimeout(() => {
        if (!isMounted) return
        if (status.value !== 'ready') {
          isOverlayVisible.value = true
        }
      }, graceDelayMs)
    }

    clockTimer = setInterval(() => {
      if (!isMounted) return
      elapsedSeconds.value = Math.floor((Date.now() - startTime) / 1000)
    }, 500)

    checkLoop()
  }

  function stopTimers() {
    if (pollTimer) {
      clearTimeout(pollTimer)
      pollTimer = null
    }
    if (clockTimer) {
      clearInterval(clockTimer)
      clockTimer = null
    }
    if (graceTimer) {
      clearTimeout(graceTimer)
      graceTimer = null
    }
  }

  function retry() {
    start(true)
  }

  onMounted(() => {
    isMounted = true
    start()
  })

  onUnmounted(() => {
    isMounted = false
    stopTimers()
  })

  return {
    status,
    isOverlayVisible,
    elapsedSeconds,
    attempts,
    lastError,
    retry,
  }
}
