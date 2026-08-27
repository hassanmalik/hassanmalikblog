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

console.log('PASS: visitor counter records once per session and renders live aggregate statistics');
