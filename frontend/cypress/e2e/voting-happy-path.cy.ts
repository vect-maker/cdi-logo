describe('Official Logo Voting — Full Happy Path', () => {
  beforeEach(() => {
    // Stub voting API endpoints for reliable, deterministic E2E execution
    cy.intercept('GET', '**/api/v1/votes/check/*', (req) => {
      req.reply({
        student_id: req.url.split('/').pop() || '21948573',
        has_voted: false,
        message: 'Carné habilitado para votar',
      })
    }).as('checkStudent')

    cy.intercept('POST', '**/api/v1/votes', (req) => {
      req.reply({
        statusCode: 201,
        body: {
          id: 1,
          receipt_id: 'ICD-VOTE-20261030-9988AABB',
          student_id: '21948573',
          student_name: 'Estudiante 21948573',
          figure_id: 'c2-matrix',
          palette_id: 'emerald',
          position_id: 'lockups',
          rationale: 'Excelente combinación geométrica. Recomendado para bordado en batas y sudaderas.',
          round: 1,
          timestamp: new Date().toISOString(),
          verification_hash: 'sha256:abc123456789def',
          has_attachment: true,
          attachment_filename: 'propuesta_estudiante.pdf',
        },
      })
    }).as('submitVote')

    cy.visit('/')
    cy.waitForAppReady()
  })

  it('completes the entire voting journey from student identification to ballot submission and receipt download', () => {
    // --- Paso 1: Identificación Estudiantil ---
    cy.get('[data-cy="student-code-input"]').type('21948573')
    cy.get('[data-cy="student-code-counter"]').should('contain.text', '8 / 8')
    cy.get('[data-cy="step1-continue-btn"]').should('not.be.disabled').click()

    // Advances to Step 2
    cy.get('[data-cy="step-indicator-2"]').should('be.visible')

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

    // Verify file dropzone is visible and attach sample PDF suggestion
    cy.get('[data-cy="file-dropzone"]').should('be.visible')
    cy.get('[data-cy="suggestion-file-input"]').selectFile(
      {
        contents: Cypress.Buffer.from('%PDF-1.4 sample proposal content'),
        fileName: 'propuesta_estudiante.pdf',
        mimeType: 'application/pdf',
      },
      { force: true }
    )
    cy.get('[data-cy="selected-file-badge"]').should('be.visible')
    cy.get('[data-cy="selected-file-name"]').should('contain.text', 'propuesta_estudiante.pdf')

    // Submit Ballot
    cy.get('[data-cy="submit-vote-btn"]').click()

    // --- Modal de Comprobante ---
    cy.get('[data-cy="receipt-modal"]').should('be.visible')
    cy.get('[data-cy="receipt-student-code"]').should('contain.text', '21948573')
    cy.get('[data-cy="receipt-figure"]').should('contain.text', 'Matrix Tensor')
    cy.get('[data-cy="receipt-palette"]').should('contain.text', 'Esmeralda & Menta')
    cy.get('[data-cy="receipt-composition"]').should('contain.text', 'Logo Horizontal')
    cy.get('[data-cy="receipt-attachment"]').should('contain.text', 'propuesta_estudiante.pdf')

    // Finalize and reset
    cy.get('[data-cy="finish-vote-btn"]').click()
    cy.get('[data-cy="receipt-modal"]').should('not.exist')

    // Back to Step 1 in pristine empty state
    cy.get('[data-cy="student-code-input"]').should('have.value', '')
    cy.get('[data-cy="step1-continue-btn"]').should('be.disabled')
  })
})
