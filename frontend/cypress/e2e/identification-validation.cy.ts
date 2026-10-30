describe('Identification Step — Validation & Barriers', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.waitForAppReady()
  })

  it('keeps continue button disabled until exactly 8 digits are entered', () => {
    // Initial state: empty input, button disabled
    cy.get('[data-cy="student-code-input"]').should('have.value', '')
    cy.get('[data-cy="student-code-counter"]').should('contain.text', '0 / 8')
    cy.get('[data-cy="step1-continue-btn"]').should('be.disabled')

    // 5 digits entered
    cy.get('[data-cy="student-code-input"]').type('12345')
    cy.get('[data-cy="student-code-counter"]').should('contain.text', '5 / 8')
    cy.get('[data-cy="step1-continue-btn"]').should('be.disabled')

    // 7 digits entered
    cy.get('[data-cy="student-code-input"]').type('67')
    cy.get('[data-cy="student-code-counter"]').should('contain.text', '7 / 8')
    cy.get('[data-cy="step1-continue-btn"]').should('be.disabled')

    // 8th digit completes valid code
    cy.get('[data-cy="student-code-input"]').type('8')
    cy.get('[data-cy="student-code-counter"]').should('contain.text', '8 / 8')
    cy.get('[data-cy="step1-continue-btn"]').should('not.be.disabled')
  })

  it('detects non-numeric characters and displays immediate error feedback', () => {
    cy.get('[data-cy="student-code-input"]').type('abc12')
    cy.get('[data-cy="student-code-error"]')
      .should('be.visible')
      .and('contain.text', 'Solo se permiten dígitos numéricos')
    cy.get('[data-cy="step1-continue-btn"]').should('be.disabled')

    // Clear and fix input
    cy.get('[data-cy="student-code-input"]').clear().type('21948573')
    cy.get('[data-cy="student-code-error"]').should('not.exist')
    cy.get('[data-cy="step1-continue-btn"]').should('not.be.disabled')
  })

  it('blocks direct navigation to later steps via header stepper when identification is missing', () => {
    // Step indicators 2, 3, 4 should be disabled when code is not valid
    cy.get('[data-cy="step-indicator-2"]').should('be.disabled')
    cy.get('[data-cy="step-indicator-3"]').should('be.disabled')
    cy.get('[data-cy="step-indicator-4"]').should('be.disabled')

    // Enter valid code
    cy.get('[data-cy="student-code-input"]').type('87654321')
    cy.get('[data-cy="step1-continue-btn"]').click()

    // Now in Step 2: Step 1 can be clicked to go back
    cy.get('[data-cy="step-indicator-1"]').should('not.be.disabled').click()
    cy.get('[data-cy="student-code-input"]').should('have.value', '87654321')
  })
})
