describe('Capture UI Screenshots', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.waitForAppReady()
  })

  it('captures all 4 wizard steps and modal on mobile and desktop', () => {
    // --- Mobile Viewport (390x844) ---
    cy.viewport(390, 844)

    // Step 1: Mobile
    cy.screenshot('mobile-step1-identification', { overwrite: true })

    // Enter code and proceed to Step 2
    cy.get('[data-cy="student-code-input"]').type('21948573')
    cy.get('[data-cy="step1-continue-btn"]').click()
    cy.get('[data-cy="figure-card-c2-matrix"]').should('be.visible')
    cy.screenshot('mobile-step2-figure-selection', { overwrite: true })

    // Select figure and go to Step 3
    cy.get('[data-cy="figure-card-c2-matrix"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()
    cy.get('[data-cy="preview-canvas"]').should('be.visible')
    cy.screenshot('mobile-step3-preview-dark', { overwrite: true })

    // Toggle athletic heather gray fabric
    cy.get('[data-cy="fabric-btn-gray"]').click()
    cy.get('[data-cy="preview-logo-img"]').should('have.attr', 'src').and('include', '-light.svg')
    cy.screenshot('mobile-step3-preview-light', { overwrite: true })

    // Step 4: Confirmation
    cy.get('[data-cy="step3-next-btn"]').click()
    cy.get('[data-cy="summary-student-code"]').should('contain.text', '21948573')
    cy.screenshot('mobile-step4-confirmation', { overwrite: true })

    // Submit and Receipt Modal
    cy.get('[data-cy="submit-vote-btn"]').click()
    cy.get('[data-cy="receipt-modal"]').should('be.visible')
    cy.screenshot('mobile-receipt-modal', { overwrite: true })

    // --- Desktop Viewport (1280x800) ---
    cy.get('[data-cy="finish-vote-btn"]').click()
    cy.viewport(1280, 800)
    cy.screenshot('desktop-step1-identification', { overwrite: true })

    cy.get('[data-cy="student-code-input"]').type('21948573')
    cy.get('[data-cy="step1-continue-btn"]').click()
    cy.get('[data-cy="figure-card-c2-matrix"]').should('be.visible')
    cy.screenshot('desktop-step2-figure-selection', { overwrite: true })

    cy.get('[data-cy="figure-card-c4-tesseract"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()
    cy.get('[data-cy="preview-canvas"]').should('be.visible')
    cy.screenshot('desktop-step3-preview-tesseract', { overwrite: true })

    cy.get('[data-cy="step3-next-btn"]').click()
    cy.get('[data-cy="summary-figure-name"]').should('contain.text', '4D Hypercube Tesseract')
    cy.screenshot('desktop-step4-confirmation', { overwrite: true })
  })
})
