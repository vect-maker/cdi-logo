describe('Official Logo Voting — Full Happy Path', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.waitForAppReady()
  })

  it('completes the entire voting journey from student identification to ballot submission and receipt download', () => {
    // --- Paso 1: Identificación Estudiantil ---
    cy.get('[data-cy="student-code-input"]').type('21948573')
    cy.get('[data-cy="student-code-counter"]').should('contain.text', '8 / 8')
    cy.get('[data-cy="step1-continue-btn"]').should('not.be.disabled').click()

    // Header updates with student badge
    cy.get('[data-cy="header-student-badge"]').should('be.visible')
    cy.get('[data-cy="header-student-code"]').should('contain.text', '21948573')

    // --- Paso 2: Selección de Figura ---
    cy.get('[data-cy="figure-card-c2-matrix"]').click()
    cy.get('[data-cy="figure-card-c2-matrix"]').should('have.class', 'solid-card-active')
    cy.get('[data-cy="step2-next-btn"]').click()

    // --- Paso 3: Color, Formato y Previsualización ---
    cy.get('[data-cy="preview-canvas"]').should('be.visible')

    // Pick Esmeralda & Menta palette
    cy.get('[data-cy="palette-option-emerald"]').click()
    cy.get('[data-cy="palette-option-emerald"]').should('have.class', 'solid-card-active')

    // Pick Logo Horizontal composition
    cy.get('[data-cy="comp-option-lockups"]').click()
    cy.get('[data-cy="comp-option-lockups"]').should('have.class', 'solid-card-active')

    // Test Dark Fabric preview (default black)
    cy.get('[data-cy="preview-logo-img"]')
      .should('have.attr', 'src')
      .and('include', '/candidates/c2-matrix/lockups/lockup-emerald.svg')

    // Test Athletic Heather Gray preview (dual-mode light variant)
    cy.get('[data-cy="fabric-btn-gray"]').click()
    cy.get('[data-cy="preview-logo-img"]')
      .should('have.attr', 'src')
      .and('include', '/candidates/c2-matrix/lockups/lockup-emerald-light.svg')

    // Switch back to black
    cy.get('[data-cy="fabric-btn-black"]').click()
    cy.get('[data-cy="preview-logo-img"]')
      .should('have.attr', 'src')
      .and('include', '/candidates/c2-matrix/lockups/lockup-emerald.svg')

    // Proceed to Step 4
    cy.get('[data-cy="step3-next-btn"]').click()

    // --- Paso 4: Confirmación y Resumen ---
    cy.get('[data-cy="summary-student-code"]').should('contain.text', '21948573')
    cy.get('[data-cy="summary-figure-name"]').should('contain.text', 'Matrix Tensor')
    cy.get('[data-cy="summary-palette-name"]').should('contain.text', 'Esmeralda & Menta')
    cy.get('[data-cy="summary-composition-name"]').should('contain.text', 'Logo Horizontal')
    cy.get('[data-cy="summary-preview-img"]').should('be.visible')

    // Add optional recommendation text
    cy.get('[data-cy="recommendations-textarea"]').type(
      'Excelente combinación geométrica. Recomendado para bordado en batas y sudaderas.'
    )

    // Submit Ballot
    cy.get('[data-cy="submit-vote-btn"]').click()

    // --- Modal de Comprobante ---
    cy.get('[data-cy="receipt-modal"]').should('be.visible')
    cy.get('[data-cy="receipt-student-code"]').should('contain.text', '21948573')
    cy.get('[data-cy="receipt-figure"]').should('contain.text', 'Matrix Tensor')
    cy.get('[data-cy="receipt-palette"]').should('contain.text', 'Esmeralda & Menta')
    cy.get('[data-cy="receipt-composition"]').should('contain.text', 'Logo Horizontal')

    // Verify receipt download button is clickable
    cy.get('[data-cy="download-receipt-btn"]').should('be.visible').click()

    // Finalize and reset
    cy.get('[data-cy="finish-vote-btn"]').click()
    cy.get('[data-cy="receipt-modal"]').should('not.exist')

    // Back to Step 1 in pristine empty state
    cy.get('[data-cy="student-code-input"]').should('have.value', '')
    cy.get('[data-cy="step1-continue-btn"]').should('be.disabled')
  })
})
