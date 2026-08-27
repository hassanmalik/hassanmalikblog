import assert from 'node:assert/strict';
import { initVisitorCounter } from '../assets/visitor-counter.mjs';

function counterFixture() {
  const visits = { textContent: '— visits' };
  const countries = { textContent: '— countries' };
  const classes = new Set();
  const root = {
    attributes: {},
    classList: {
      add: (...names) => names.forEach((name) => classes.add(name)),
      remove: (...names) => names.forEach((name) => classes.delete(name)),
    },
    querySelector: (selector) => selector === '[data-visit-count]' ? visits : countries,
    setAttribute(name, value) { this.attributes[name] = value; },
  };
  return { root, visits, countries, classes };
}

const first = counterFixture();
const second = counterFixture();
const documentRef = { querySelectorAll: () => [first.root, second.root] };
const stored = new Map();
const storage = {
  getItem: (key) => stored.get(key) ?? null,
  setItem: (key, value) => stored.set(key, value),
};
const calls = [];
const fetchImpl = async (url, options = {}) => {
  calls.push({ url, method: options.method ?? 'GET' });
  return {
    ok: true,
    json: async () => ({ visits: 1284, countries: 23, topCountries: [] }),
  };
};

await initVisitorCounter({ documentRef, fetchImpl, storage });

assert.deepEqual(calls.map(({ method }) => method), ['POST', 'GET']);
assert.equal(calls[0].url, 'https://blog-counter.hassanmalik1989.workers.dev/visit');
assert.equal(calls[1].url, 'https://blog-counter.hassanmalik1989.workers.dev/stats');
assert.equal(first.visits.textContent, '1,284 visits');
assert.equal(first.countries.textContent, '23 countries');
assert.equal(second.visits.textContent, '1,284 visits');
assert.equal(first.root.attributes['aria-label'], '1,284 total visits from 23 countries');
assert(first.classes.has('is-loaded'));
assert.equal(stored.get('hm-visit-recorded-v1'), 'true');

calls.length = 0;
await initVisitorCounter({ documentRef, fetchImpl, storage });
assert.deepEqual(calls.map(({ method }) => method), ['GET']);

const unavailable = counterFixture();
await initVisitorCounter({
  documentRef: { querySelectorAll: () => [unavailable.root] },
  fetchImpl: async () => { throw new Error('offline'); },
  storage: { getItem: () => 'true', setItem: () => {} },
});
assert.equal(unavailable.visits.textContent, '— visits');
assert.equal(unavailable.countries.textContent, '— countries');
assert.equal(unavailable.root.attributes['aria-label'], 'Visitor statistics unavailable');
assert(unavailable.classes.has('is-unavailable'));

const malformed = counterFixture();
await initVisitorCounter({
  documentRef: { querySelectorAll: () => [malformed.root] },
  fetchImpl: async () => ({
    ok: true,
    json: async () => ({ visits: '0', countries: 0, topCountries: [] }),
  }),
  storage: { getItem: () => 'true', setItem: () => {} },
});
assert.equal(malformed.root.attributes['aria-label'], 'Visitor statistics unavailable');
assert(malformed.classes.has('is-unavailable'));

const slowWrite = counterFixture();
let releaseVisit;
let confirmStatsRequested;
const statsRequested = new Promise((resolve) => { confirmStatsRequested = resolve; });
const slowRun = initVisitorCounter({
  documentRef: { querySelectorAll: () => [slowWrite.root] },
  fetchImpl: async (url) => {
    if (url.endsWith('/visit')) {
      return new Promise((resolve) => { releaseVisit = () => resolve({ ok: true }); });
    }
    confirmStatsRequested();
    return {
      ok: true,
      json: async () => ({ visits: 1, countries: 1, topCountries: [] }),
    };
  },
  storage: { getItem: () => null, setItem: () => {} },
});
await Promise.race([
  statsRequested,
  new Promise((_, reject) => setTimeout(() => reject(new Error('stats read blocked by visit write')), 100)),
]);
await new Promise((resolve) => setTimeout(resolve, 0));
assert.equal(slowWrite.visits.textContent, '1 visit');
assert.equal(slowWrite.countries.textContent, '1 country');
assert.equal(slowWrite.root.attributes['aria-label'], '1 total visit from 1 country');
releaseVisit();
await slowRun;

const failedWriteCalls = [];
const failedWriteStore = new Map();
const failedWriteStorage = {
  getItem: (key) => failedWriteStore.get(key) ?? null,
  setItem: (key, value) => failedWriteStore.set(key, value),
};
const failedWriteFetch = async (url, options = {}) => {
  const method = options.method ?? 'GET';
  failedWriteCalls.push(method);
  if (url.endsWith('/visit')) return { ok: false, status: 503 };
  return {
    ok: true,
    json: async () => ({ visits: 9, countries: 2, topCountries: [] }),
  };
};
await initVisitorCounter({ documentRef, fetchImpl: failedWriteFetch, storage: failedWriteStorage });
await initVisitorCounter({ documentRef, fetchImpl: failedWriteFetch, storage: failedWriteStorage });
assert.deepEqual(failedWriteCalls, ['POST', 'GET', 'GET']);
assert.equal(failedWriteStore.get('hm-visit-recorded-v1'), 'true');

console.log('PASS: visitor counter records once per session and renders live aggregate statistics');
