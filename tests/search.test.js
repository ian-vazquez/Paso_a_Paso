/**
 * Tests for src/search.js. Run with `npm test` (node --test, no dependencies).
 *
 * Each entry here carries only the fields search.js reads.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { toISODate, isOpenNow, openNow, openingSoon } from '../src/search.js';

const entry = (fields) => ({ name: 'X', cycle_status: 'open', deadline: null, opens_month: null, ...fields });
const names = (list) => list.map((e) => e.name);

test('toISODate uses the local calendar day', () => {
  assert.equal(toISODate(new Date(2026, 11, 5)), '2026-12-05');
});

test('an open entry stays open through its deadline day, then drops out', () => {
  const bk = entry({ name: 'Burger King', deadline: '2026-12-15' });
  assert.equal(isOpenNow(bk, '2026-12-14'), true);
  assert.equal(isOpenNow(bk, '2026-12-15'), true);
  assert.equal(isOpenNow(bk, '2026-12-16'), false);
});

test('upcoming and unknown entries are not open now; rolling is', () => {
  assert.equal(isOpenNow(entry({ cycle_status: 'upcoming' }), '2026-11-17'), false);
  assert.equal(isOpenNow(entry({ cycle_status: 'unknown' }), '2026-11-17'), false);
  assert.equal(isOpenNow(entry({ cycle_status: 'rolling' }), '2026-11-17'), true);
});

test('openNow sorts by deadline, with no-deadline entries last', () => {
  const list = [
    entry({ name: 'Rolling', cycle_status: 'rolling' }),
    entry({ name: 'Feb', deadline: '2027-02-15' }),
    entry({ name: 'Dec', deadline: '2026-12-15' }),
    entry({ name: 'Expired', deadline: '2026-11-01' }),
  ];
  assert.deepEqual(names(openNow(list, '2026-11-17')), ['Dec', 'Feb', 'Rolling']);
});

test('openingSoon groups by month, rolling into next year, unknown month last', () => {
  const list = [
    entry({ name: 'NoMonth', cycle_status: 'upcoming' }),
    entry({ name: 'Jan', cycle_status: 'upcoming', opens_month: 1 }),
    entry({ name: 'Dec', cycle_status: 'upcoming', opens_month: 12 }),
    entry({ name: 'Open', cycle_status: 'open', opens_month: 1 }),
  ];
  const groups = openingSoon(list, '2026-11-17');
  assert.deepEqual(
    groups.map((g) => [g.month, g.year, names(g.entries)]),
    [
      [12, 2026, ['Dec']],
      [1, 2027, ['Jan']],
      [null, null, ['NoMonth']],
    ]
  );
});

test('openingSoon leaves out an upcoming entry whose deadline has passed', () => {
  const list = [entry({ name: 'Stale', cycle_status: 'upcoming', deadline: '2026-10-01' })];
  assert.deepEqual(openingSoon(list, '2026-11-17'), []);
});
