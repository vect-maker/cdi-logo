import './commands'

beforeEach(() => {
  // Global default: instant healthy backend unless spec intercepts with an alias
  cy.intercept('GET', '**/health', (req) => {
    if (!req.alias) {
      req.reply({
        statusCode: 200,
        body: { status: 'ok', app: 'ICD Logo Voting API', round: 1, database: 'sqlite-fallback' },
      })
    }
  })

  // Global default: allow valid 8-digit students to vote unless specific spec overrides
  cy.intercept('GET', '**/api/v1/votes/check/*', (req) => {
    if (!req.alias) {
      req.reply({
        student_id: req.url.split('/').pop() || '20260001',
        has_voted: false,
        message: 'Carné habilitado para votar',
      })
    }
  })
})
