describe('Backend Cold-Start Wakeup & Polling UX', () => {
  it('does not flash overlay when backend is already healthy and responds immediately', () => {
    cy.intercept('GET', '**/health', {
      statusCode: 200,
      body: {
        status: 'ok',
        app: 'ICD Logo Voting API',
        round: 1,
        database: 'sqlite-fallback',
      },
    }).as('fastHealth')

    cy.visit('/')
    cy.wait('@fastHealth')

    // Overlay is never displayed due to debounce grace period
    cy.get('[data-cy="server-wakeup-overlay"]').should('not.exist')
    cy.get('[data-cy="student-code-input"]').should('be.visible')
  })

  it('displays cold-start wakeup overlay when backend is sleeping and resolves to Step 1 on 200 OK', () => {
    let callCount = 0

    // Intercept /health: first 2 attempts fail/hang, 3rd attempt succeeds
    cy.intercept('GET', '**/health', (req) => {
      callCount++
      if (callCount < 3) {
        req.reply({
          statusCode: 503,
          body: { error: 'Service Unavailable - Container Starting' },
        })
      } else {
        req.reply({
          statusCode: 200,
          body: {
            status: 'ok',
            app: 'ICD Logo Voting API',
            round: 1,
            database: 'sqlite-fallback',
          },
        })
      }
    }).as('healthCheck')

    cy.visit('/')

    // Verify overlay appears with waking-up status
    cy.get('[data-cy="server-wakeup-overlay"]').should('be.visible')
    cy.get('[data-cy="server-status-title"]').should('contain.text', 'Iniciando Servidor')
    cy.get('[data-cy="server-status-desc"]').should('contain.text', 'reactivándose')

    // Wait for successful 3rd call
    cy.wait('@healthCheck')
    cy.wait('@healthCheck')
    cy.wait('@healthCheck')

    // Overlay dissolves and Step 1 becomes visible
    cy.get('[data-cy="server-wakeup-overlay"]', { timeout: 10000 }).should('not.exist')
    cy.get('[data-cy="student-code-input"]').should('be.visible')
  })

  it('displays timeout error screen if backend does not wake up within timeout, allowing retry', () => {
    let isRetrying = false

    cy.intercept('GET', '**/health', (req) => {
      if (!isRetrying) {
        req.reply({
          statusCode: 503,
          body: { error: 'Service Unavailable' },
        })
      } else {
        req.reply({
          statusCode: 200,
          body: {
            status: 'ok',
            app: 'ICD Logo Voting API',
            round: 1,
            database: 'sqlite-fallback',
          },
        })
      }
    }).as('timeoutHealthCheck')

    // Visit with fast test timeout parameters
    cy.visit('/?serverTimeoutMs=1200&serverIntervalMs=250')

    // Verify overlay is visible
    cy.get('[data-cy="server-wakeup-overlay"]').should('be.visible')

    // Wait for timeout to elapse into 'timeout' state
    cy.get('[data-cy="server-status-title"]', { timeout: 8000 }).should('contain.text', 'No se pudo conectar')
    cy.get('[data-cy="retry-connection-btn"]').should('be.visible')

    // Set flag and click retry to allow subsequent health check to succeed
    cy.get('[data-cy="retry-connection-btn"]').then(($btn) => {
      isRetrying = true
      cy.wrap($btn).click()
    })

    // Overlay dissolves and Step 1 is ready
    cy.get('[data-cy="server-wakeup-overlay"]', { timeout: 10000 }).should('not.exist')
    cy.get('[data-cy="student-code-input"]').should('be.visible')
  })
})
