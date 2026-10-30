import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  HealthResponseSchema,
  StudentIdSchema,
  SubmitVoteRequestSchema,
  VoteReceiptResponseSchema,
  ErrorPayloadSchema,
} from './index';

describe('API & Zod Schemas Validation', () => {
  describe('HealthResponseSchema', () => {
    it('validates a successful health check payload from FastAPI', () => {
      const payload = {
        status: 'ok',
        app: 'ICD Logo Voting API',
        round: 1,
        database: 'turso-libsql',
      };
      const result = HealthResponseSchema.parse(payload);
      assert.equal(result.status, 'ok');
      assert.equal(result.round, 1);
      assert.equal(result.database, 'turso-libsql');
    });
  });

  describe('StudentIdSchema (8 digits)', () => {
    it('accepts valid 8-digit student ID', () => {
      assert.equal(StudentIdSchema.parse('20260001'), '20260001');
      assert.equal(StudentIdSchema.parse(' 12345678 '), '12345678');
    });

    it('rejects IDs shorter or longer than 8 digits', () => {
      assert.throws(() => StudentIdSchema.parse('1234567'));
      assert.throws(() => StudentIdSchema.parse('123456789'));
    });

    it('rejects IDs with non-digit characters', () => {
      assert.throws(() => StudentIdSchema.parse('2026000A'));
      assert.throws(() => StudentIdSchema.parse('2026-001'));
    });
  });

  describe('SubmitVoteRequestSchema', () => {
    it('validates a complete, valid vote payload', () => {
      const payload = {
        student_id: '20260001',
        student_name: 'María Flores',
        figure_id: 'c4-tesseract',
        palette_id: 'cobalt',
        position_id: 'chest-center',
        rationale: 'Excelente contraste y equilibrio.',
      };
      const parsed = SubmitVoteRequestSchema.parse(payload);
      assert.equal(parsed.student_id, '20260001');
      assert.equal(parsed.figure_id, 'c4-tesseract');
      assert.equal(parsed.palette_id, 'cobalt');
      assert.equal(parsed.position_id, 'chest-center');
    });

    it('rejects payloads with invalid figure or palette', () => {
      assert.throws(() =>
        SubmitVoteRequestSchema.parse({
          student_id: '20260001',
          student_name: 'María Flores',
          figure_id: 'c99-invalid',
          palette_id: 'cobalt',
          position_id: 'chest-center',
        })
      );
    });

    it('defaults rationale to empty string if omitted', () => {
      const parsed = SubmitVoteRequestSchema.parse({
        student_id: '20260001',
        student_name: 'Carlos Ruiz',
        figure_id: 'c2-matrix',
        palette_id: 'dark',
        position_id: 'sleeve-left',
      });
      assert.equal(parsed.rationale, '');
    });
  });

  describe('VoteReceiptResponseSchema', () => {
    it('parses receipt with verification hash', () => {
      const receipt = {
        receipt_id: 'VOTE-20261029-A1B2C3D4',
        student_id: '20260001',
        student_name: 'María Flores',
        figure_id: 'c4-tesseract',
        palette_id: 'cobalt',
        position_id: 'chest-center',
        timestamp: '2026-10-29T21:00:00Z',
        round: 1,
        verification_hash: 'sha256:abcdef1234567890',
      };
      const parsed = VoteReceiptResponseSchema.parse(receipt);
      assert.equal(parsed.receipt_id, 'VOTE-20261029-A1B2C3D4');
      assert.equal(parsed.round, 1);
    });
  });

  describe('ErrorPayloadSchema', () => {
    it('parses standard backend error responses', () => {
      const errorData = {
        message: 'El carné ya ha emitido su voto en esta ronda',
        code: 'ALREADY_VOTED',
      };
      const parsed = ErrorPayloadSchema.parse(errorData);
      assert.equal(parsed.message, 'El carné ya ha emitido su voto en esta ronda');
      assert.equal(parsed.code, 'ALREADY_VOTED');
    });
  });
});
