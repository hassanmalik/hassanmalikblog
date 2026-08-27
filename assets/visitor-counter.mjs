const WORKER_ORIGIN = 'https://blog-counter.hassanmalik1989.workers.dev';
const SESSION_KEY = 'hm-visit-recorded-v1';
const numberFormat = new Intl.NumberFormat('en-US');

function renderStats(counters, stats) {
  const visits = stats.visits;
  const countries = stats.countries;
  const visitText = `${numberFormat.format(visits)} ${visits === 1 ? 'visit' : 'visits'}`;
  const countryText = `${numberFormat.format(countries)} ${countries === 1 ? 'country' : 'countries'}`;

  counters.forEach((counter) => {
    counter.querySelector('[data-visit-count]').textContent = visitText;
    counter.querySelector('[data-country-count]').textContent = countryText;
    counter.setAttribute('aria-label', `${numberFormat.format(visits)} total ${visits === 1 ? 'visit' : 'visits'} from ${numberFormat.format(countries)} ${countries === 1 ? 'country' : 'countries'}`);
    counter.classList.remove('is-unavailable');
    counter.classList.add('is-loaded');
  });
}

function hasValidStats(stats) {
  return stats
    && Number.isSafeInteger(stats.visits)
    && stats.visits >= 0
    && Number.isSafeInteger(stats.countries)
    && stats.countries >= 0;
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

  const recordVisit = async () => {
    if (recorded) return;
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
  };

  const loadStats = async () => {
    try {
      const response = await fetchImpl(`${WORKER_ORIGIN}/stats`, {
        credentials: 'omit',
      });
      if (!response.ok) throw new Error(`Statistics request failed: ${response.status}`);
      const stats = await response.json();
      if (!hasValidStats(stats)) throw new Error('Invalid statistics response');
      renderStats(counters, stats);
    } catch {
      renderUnavailable(counters);
    }
  };

  await Promise.all([recordVisit(), loadStats()]);
}

if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  initVisitorCounter();
}
