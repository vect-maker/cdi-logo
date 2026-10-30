import './commands'

beforeEach(() => {
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
