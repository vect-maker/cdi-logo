import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { useHealthApi } from './modules/health/useHealthApi';

describe('useHealthApi Integration Check', () => {
  it('connects to FastAPI backend and parses health response via Zod', async () => {
    const { getHealth } = useHealthApi();
    const res = await getHealth();

    assert.equal(res.status, 'ok');
    assert.equal(res.round, 1);
    assert.ok(res.app?.includes('ICD Logo Voting'));
  });
});
