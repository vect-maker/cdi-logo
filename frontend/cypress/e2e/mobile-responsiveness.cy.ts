describe('Mobile Responsiveness & Viewport UX (390x844)', () => {
  beforeEach(() => {
    cy.viewport(390, 844)
    cy.visit('/')
    cy.waitForAppReady()
  })

  it('renders a compact header stepper without horizontal overflow or clipping', () => {
    cy.get('[data-cy="stepper-nav"]').should('be.visible')
    cy.window().then((win) => {
      expect(win.document.documentElement.scrollWidth).to.be.lte(390)
    })
  })

  it('organizes candidate figures into a 2-column mobile grid in Step 2', () => {
    cy.enterStudentCode('98765432')

    // Verify grid has 6 cards visible
    cy.get('[data-cy^="figure-card-"]').should('have.length', 6)

    // Verify first two cards sit side-by-side horizontally (same Y offset, different X offset)
    cy.get('[data-cy="figure-card-c1-neural"]').then(($card1) => {
      cy.get('[data-cy="figure-card-c2-matrix"]').then(($card2) => {
        const rect1 = $card1[0].getBoundingClientRect()
        const rect2 = $card2[0].getBoundingClientRect()
        expect(Math.abs(rect1.top - rect2.top)).to.be.lessThan(10)
        expect(rect2.left).to.be.greaterThan(rect1.left)
      })
    })
  })

  it('places preview canvas above selectors (order-1) on mobile for instant visual feedback', () => {
    cy.enterStudentCode('98765432')
    cy.get('[data-cy="figure-card-c4-tesseract"]').click()
    cy.get('[data-cy="step2-next-btn"]').click()

    // Assert the preview canvas is positioned ABOVE the palette options in mobile layout
    cy.get('[data-cy="preview-canvas"]').then(($canvas) => {
      cy.get('[data-cy="palette-option-cobalt"]').then(($palette) => {
        const canvasRect = $canvas[0].getBoundingClientRect()
        const paletteRect = $palette[0].getBoundingClientRect()
        expect(canvasRect.bottom).to.be.lessThan(paletteRect.top)
      })
    })

    // Tapping a palette immediately updates the preview image at the top
    cy.get('[data-cy="palette-option-violet"]').click()
    cy.get('[data-cy="preview-logo-img"]')
      .should('have.attr', 'src')
      .and('include', '-violet.svg')
  })

  it('renders full-width ergonomic action buttons on Step 4', () => {
    cy.enterStudentCode('98765432')
    cy.get('[data-cy="step2-next-btn"]').click()
    cy.get('[data-cy="step3-next-btn"]').click()

    cy.get('[data-cy="submit-vote-btn"]').then(($btn) => {
      const rect = $btn[0].getBoundingClientRect()
      // Button should span nearly the full content container width on mobile
      expect(rect.width).to.be.greaterThan(300)
      expect(rect.height).to.be.gte(44) // Meets WCAG minimum touch target size
    })
  })
})
