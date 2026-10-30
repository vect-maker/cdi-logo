import { defineConfig } from 'cypress'

export default defineConfig({
  screenshotOnRunFailure: false,
  e2e: {
    baseUrl: 'http://localhost:5173',
    specPattern: ['cypress/e2e/**/*.cy.ts', 'cypress/visual/**/*.cy.ts'],
    supportFile: 'cypress/support/e2e.ts',
    viewportWidth: 390,
    viewportHeight: 844,
    video: false,
  },
})
