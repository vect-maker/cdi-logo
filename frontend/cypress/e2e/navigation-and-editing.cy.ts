describe('Navigation & Reversible Editing Workflows', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.waitForAppReady()
    cy.enterStudentCode('31415926')
  })

  it('preserves state when using "Atrás" buttons backwards and forwards', () => {
    // Select C3 Hexcore in Step 2
    cy.get('[data-cy="figure-card-c3-hexcore"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()

    // Select Violet palette and Centered Stacked logo in Step 3
    cy.get('[data-cy="palette-option-violet"]').click()
    cy.get('[data-cy="comp-option-stacked"]').click()

    // Go back to Step 2 using "Atrás"
    cy.get('[data-cy="step3-back-btn"]').click()
    cy.get('[data-cy="figure-card-c3-hexcore"]').should('have.class', 'solid-card-active')

    // Go back to Step 1 using "Atrás"
    cy.get('[data-cy="step2-back-btn"]').click()
    cy.get('[data-cy="student-code-input"]').should('have.value', '31415926')

    // Forward back to Step 3 and confirm options remained selected
    cy.get('[data-cy="step1-continue-btn"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()
    cy.get('[data-cy="palette-option-violet"]').should('have.class', 'solid-card-active')
    cy.get('[data-cy="comp-option-stacked"]').should('have.class', 'solid-card-active')
  })

  it('allows fast-travel editing from Step 4 summary via "Cambiar" buttons', () => {
    // Setup initial selections: C1 Neural, Emerald, Lockups
    cy.get('[data-cy="figure-card-c1-neural"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()
    cy.get('[data-cy="palette-option-emerald"]').click()
    cy.get('[data-cy="comp-option-lockups"]').click()
    cy.get('[data-cy="step3-next-btn"]').click()

    // Verify initial summary
    cy.get('[data-cy="summary-figure-name"]').should('contain.text', 'Neural Cluster')
    cy.get('[data-cy="summary-palette-name"]').should('contain.text', 'Esmeralda & Menta')

    // Click "Cambiar" on Figure -> Jumps directly to Step 2
    cy.get('[data-cy="change-figure-btn"]').click()
    cy.get('[data-cy="figure-card-c6-waveform"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()
    cy.get('[data-cy="step3-next-btn"]').click()

    // Verify summary updated to C6 Harmonized Waveform
    cy.get('[data-cy="summary-figure-name"]').should('contain.text', 'Harmonized Waveform')
    cy.get('[data-cy="summary-palette-name"]').should('contain.text', 'Esmeralda & Menta')

    // Click "Cambiar" on Palette -> Jumps directly to Step 3
    cy.get('[data-cy="change-palette-btn"]').click()
    cy.get('[data-cy="palette-option-amber"]').click()
    cy.get('[data-cy="step3-next-btn"]').click()

    // Verify summary updated to Ámbar & Naranja
    cy.get('[data-cy="summary-palette-name"]').should('contain.text', 'Ámbar & Naranja')
  })
})
