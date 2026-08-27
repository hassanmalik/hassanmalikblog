const WORKER_ORIGIN = 'https://blog-counter.hassanmalik1989.workers.dev';
const SESSION_KEY = 'hm-visit-recorded-v1';
const numberFormat = new Intl.NumberFormat('en-US');

function renderStats(counters, stats) {
  const visits = Math.max(0, Number(stats.visits) || 0);
  const countries = Math.max(0, Number(stats.countries) || 0);
  const visitText = `${numberFormat.format(visits)} ${visits === 1 ? 'visit' : 'visits'}`;
  const countryText = `${numberFormat.format(countries)} ${countries === 1 ? 'country' : 'countries'}`;

  counters.forEach((counter) => {
    counter.querySelector('[data-visit-count]').textContent = visitText;
    counter.querySelector('[data-country-count]').textContent = countryText;
    counter.setAttribute('aria-label', `${numberFormat.format(visits)} total visits from ${numberFormat.format(countries)} countries`);
    counter.classList.remove('is-unavailable');
    counter.classList.add('is-loaded');
  });
}

function renderUnavailable(counters) {
  counters.forEach((counter) => {
    counter.setAttribute('aria-label', 'Visitor statistics unavailable');
    counter.classList.remove('is-loaded');
    counter.classList.add('is-unavailable');
  });
}

export async function initVisitorCounter({
  documentRef = document,
  fetchImpl = fetch,
  storage = sessionStorage,
} = {}) {
  const counters = [...documentRef.querySelectorAll('[data-visitor-counter]')];
  if (!counters.length) return;

  let recorded = false;
  try {
    recorded = storage.getItem(SESSION_KEY) === 'true';
  } catch {
    // A blocked storage API should not prevent anonymous aggregate counting.
  }

  if (!recorded) {
    try {
      const response = await fetchImpl(`${WORKER_ORIGIN}/visit`, {
        method: 'POST',
        credentials: 'omit',
      });
      if (response.ok) {
        try { storage.setItem(SESSION_KEY, 'true'); } catch { /* Storage is optional. */ }
      }
    } catch {
      // Statistics can still load when the write endpoint is temporarily unavailable.
    }
  }

  try {
    const response = await fetchImpl(`${WORKER_ORIGIN}/stats`, {
      credentials: 'omit',
    });
    if (!response.ok) throw new Error(`Statistics request failed: ${response.status}`);
    renderStats(counters, await response.json());
  } catch {
    renderUnavailable(counters);
  }
}

if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  initVisitorCounter();
}
