<script setup lang="ts">
import { useVotingStore } from './stores/votingStore'
import WizardHeader from './components/WizardHeader.vue'
import Step1Identification from './components/Step1Identification.vue'
import Step2FigureSelection from './components/Step2FigureSelection.vue'
import Step3PalettePosition from './components/Step3PalettePosition.vue'
import Step4Confirmation from './components/Step4Confirmation.vue'
import ReceiptModal from './components/ReceiptModal.vue'

const store = useVotingStore()
</script>

<template>
  <div class="min-h-screen bg-[#0b1120] text-slate-100 flex flex-col relative selection:bg-blue-600 selection:text-white">
    <!-- Fixed Header Bar -->
    <WizardHeader />

    <!-- Main Wizard Content Canvas -->
    <main class="flex-1 max-w-6xl w-full mx-auto px-3 sm:px-6 pb-6 sm:pb-10 relative z-10">
      <Step1Identification v-if="store.currentStep === 1" key="step1" />
      <Step2FigureSelection v-else-if="store.currentStep === 2" key="step2" />
      <Step3PalettePosition v-else-if="store.currentStep === 3" key="step3" />
      <Step4Confirmation v-else-if="store.currentStep === 4" key="step4" />
    </main>

    <!-- Success Modal Receipt -->
    <ReceiptModal />
  </div>
</template>

<style scoped>
.fade-step-enter-active,
.fade-step-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-step-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.fade-step-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
