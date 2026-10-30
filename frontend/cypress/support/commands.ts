declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Waits for the voting application header to be fully mounted and visible.
       */
      waitForAppReady(): Chainable<void>
      /**
       * Fills in the 8-digit student identification code and proceeds to Step 2.
       */
      enterStudentCode(code: string): Chainable<void>
    }
  }
}

Cypress.Commands.add('waitForAppReady', () => {
  cy.get('[data-cy="header-title"]', { timeout: 10000 }).should('be.visible')
})

Cypress.Commands.add('enterStudentCode', (code: string) => {
  cy.get('[data-cy="student-code-input"]').clear().type(code)
  cy.get('[data-cy="step1-continue-btn"]').should('not.be.disabled').click()
  cy.get('[data-cy="figure-card-c1-neural"]', { timeout: 5000 }).should('be.visible')
})

export {}
