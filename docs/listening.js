const ASSET_PREFIX = (() => {
  if (window.location.hostname.endsWith('github.io')) {
    const [repoName = ''] = window.location.pathname.split('/').filter(Boolean);
    return repoName ? `/${repoName}` : '';
  }
  return '';
})();
const ASSET_VERSION = '20260328-random-scope-1';

const UNIT_CONFIG = {
  U01: { label: 'UNIT 1', csv: '/data/eijukugo_zukan/units/U01/dataset.csv' },
  U02: { label: 'UNIT 2', csv: '/data/eijukugo_zukan/units/U02/dataset.csv' },
  U03: { label: 'UNIT 3', csv: '/data/eijukugo_zukan/units/U03/dataset.csv' },
  U04: { label: 'UNIT 4', csv: '/data/eijukugo_zukan/units/U04/dataset.csv' },
  U05: { label: 'UNIT 5', csv: '/data/eijukugo_zukan/units/U05/dataset.csv' },
  U06: { label: 'UNIT 6', csv: '/data/eijukugo_zukan/units/U06/dataset.csv' },
  U07: { label: 'UNIT 7', csv: '/data/eijukugo_zukan/units/U07/dataset.csv' },
  U08: { label: 'UNIT 8', csv: '/data/eijukugo_zukan/units/U08/dataset.csv' },
  U09: { label: 'UNIT 9', csv: '/data/eijukugo_zukan/units/U09/dataset.csv' },
  U10: { label: 'UNIT 10', csv: '/data/eijukugo_zukan/units/U10/dataset.csv' },
  U11: { label: 'UNIT 11', csv: '/data/eijukugo_zukan/units/U11/dataset.csv' },
  U12: { label: 'UNIT 12', csv: '/data/eijukugo_zukan/units/U12/dataset.csv' },
  U13: { label: 'UNIT 13', csv: '/data/eijukugo_zukan/units/U13/dataset.csv' },
  U14: { label: 'UNIT 14', csv: '/data/eijukugo_zukan/units/U14/dataset.csv' },
  U15: { label: 'UNIT 15', csv: '/data/eijukugo_zukan/units/U15/dataset.csv' },
  U16: { label: 'UNIT 16', csv: '/data/eijukugo_zukan/units/U16/dataset.csv' },
  U17: { label: 'UNIT 17', csv: '/data/eijukugo_zukan/units/U17/dataset.csv' },
  U18: { label: 'UNIT 18', csv: '/data/eijukugo_zukan/units/U18/dataset.csv' },
  U19: { label: 'UNIT 19', csv: '/data/eijukugo_zukan/units/U19/dataset.csv' },
  U20: { label: 'UNIT 20', csv: '/data/eijukugo_zukan/units/U20/dataset.csv' },
  U21: { label: 'UNIT 21', csv: '/data/eijukugo_zukan/units/U21/dataset.csv' },
};

const el = {
  unitTabs: document.getElementById('unitTabs'),
  btnScopeAll: document.getElementById('btnScopeAll'),
  btnScopeRandom: document.getElementById('btnScopeRandom'),
  btnScopeMust: document.getElementById('btnScopeMust'),
  btnBackToStudy: document.getElementById('btnBackToStudy'),
  qImg: document.getElementById('qImg'),
  guide: document.getElementById('guide'),
  hintCloze: document.getElementById('hintCloze'),
  btnHintCloze: document.getElementById('btnHintCloze'),
  btnCheck: document.getElementById('btnCheck'),
  btnNext: document.getElementById('btnNext'),
  fb: document.getElementById('fb'),
  answerBox: document.getElementById('answerBox'),
  aEn: document.getElementById('aEn'),
  aIpa: document.getElementById('aIpa'),
  aJp: document.getElementById('aJp'),
  jpAnswer: document.getElementById('jpAnswer'),
  memoryActions: document.getElementById('memoryActions'),
  btnRemembered: document.getElementById('btnRemembered'),
  btnPending: document.getElementById('btnPending'),
  btnUnknown: document.getElementById('btnUnknown'),
  audioPlayer: document.getElementById('audioPlayer'),
  playbackRate: document.getElementById('playbackRate'),
};

const state = {
  unit: 'U01',
  scope: loadScope(),
  rows: [],
  p: 0,
  cache: {},
  statuses: loadStatuses(),
  hintClozeVisible: false,
  playbackRate: loadPlaybackRate(),
};

function parseCsv(text) {
  const src = text.replace(/^\ufeff/, '');
  const rows = [];
  let row = [];
  let field = '';
  let i = 0;
  let inQuotes = false;
  while (i < src.length) {
    const ch = src[i];
    const nx = src[i + 1];
    if (inQuotes) {
      if (ch === '"' && nx === '"') {
        field += '"';
        i += 2;
        continue;
      }
      if (ch === '"') {
        inQuotes = false;
        i += 1;
        continue;
      }
      field += ch;
      i += 1;
      continue;
    }
    if (ch === '"') {
      inQuotes = true;
      i += 1;
      continue;
    }
    if (ch === ',') {
      row.push(field);
      field = '';
      i += 1;
      continue;
    }
    if (ch === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
      i += 1;
      continue;
    }
    if (ch === '\r') {
      i += 1;
      continue;
    }
    field += ch;
    i += 1;
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  const [header, ...body] = rows;
  return body
    .filter((r) => r.length >= header.length)
    .map((r) => header.reduce((acc, key, idx) => {
      acc[key] = r[idx] || '';
      return acc;
    }, {}));
}

function assetPath(path) {
  if (!path) return '';
  const separator = path.includes('?') ? '&' : '?';
  return `${ASSET_PREFIX}${path}${separator}v=${ASSET_VERSION}`;
}

function loadStatuses() {
  try {
    return JSON.parse(window.localStorage.getItem('eizukan_listening_statuses_v1') || '{}');
  } catch {
    return {};
  }
}

function saveStatuses() {
  window.localStorage.setItem('eizukan_listening_statuses_v1', JSON.stringify(state.statuses));
}

function loadScope() {
  try {
    const saved = window.localStorage.getItem('eizukan_listening_scope_v1');
    return saved === 'must' || saved === 'random' ? saved : 'all';
  } catch {
    return 'all';
  }
}

function saveScope() {
  window.localStorage.setItem('eizukan_listening_scope_v1', state.scope);
}

function loadPlaybackRate() {
  try {
    const value = Number(window.localStorage.getItem('eizukan_listening_rate_v1') || '1');
    return Number.isFinite(value) ? value : 1;
  } catch {
    return 1;
  }
}

function savePlaybackRate() {
  window.localStorage.setItem('eizukan_listening_rate_v1', String(state.playbackRate));
}

function rowKey(row) {
  return `${row.chapter || state.unit}:${row.qno}`;
}

function statusOf(row) {
  return state.statuses[rowKey(row)] || '';
}

function isMustRow(row) {
  return statusOf(row) !== 'remembered';
}

function activeRows() {
  return state.scope === 'must' ? state.rows.filter(isMustRow) : state.rows;
}

function currentRow() {
  return activeRows()[state.p];
}

function displayJapanese(row) {
  return row.japanese || row.english || '';
}

function feedback(msg, ok) {
  el.fb.textContent = msg;
  el.fb.classList.remove('ok', 'ng');
  if (ok === true) el.fb.classList.add('ok');
  if (ok === false) el.fb.classList.add('ng');
}

function renderUnitButtons() {
  el.unitTabs.innerHTML = Object.entries(UNIT_CONFIG)
    .map(([unit, config]) => `<button type="button" data-unit="${unit}">${config.label}</button>`)
    .join('');
}

function shuffleRows(rows) {
  const copy = [...rows];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

async function ensureUnitRows(unit) {
  if (state.cache[unit]) return state.cache[unit];
  const res = await fetch(assetPath(UNIT_CONFIG[unit].csv), { cache: 'no-store' });
  const txt = await res.text();
  const rows = parseCsv(txt);
  state.cache[unit] = rows;
  return rows;
}

async function ensureAllRows() {
  return (await Promise.all(Object.keys(UNIT_CONFIG).map((unit) => ensureUnitRows(unit)))).flat();
}

function syncUnitButtons() {
  const activeUnit = state.scope === 'random' ? '' : state.unit;
  [...el.unitTabs.querySelectorAll('button[data-unit]')].forEach((button) => {
    button.classList.toggle('active', button.dataset.unit === activeUnit);
  });
}

async function setUnit(unit) {
  state.unit = unit;
  window.localStorage.setItem('eizukan_listening_unit_v1', unit);
  syncUnitButtons();
  if (state.scope !== 'random') {
    state.rows = await ensureUnitRows(unit);
  }
  state.p = 0;
  render();
}

function render() {
  const row = currentRow();
  el.btnScopeAll.classList.toggle('active', state.scope === 'all');
  el.btnScopeRandom.classList.toggle('active', state.scope === 'random');
  el.btnScopeMust.classList.toggle('active', state.scope === 'must');

  if (!row) {
    el.qImg.removeAttribute('src');
    el.guide.textContent = state.scope === 'must'
      ? 'MUST に表示できるカードがありません。ALL に切り替えると全問題を表示できます。'
      : '表示できるカードがありません。';
    el.answerBox.hidden = true;
    el.memoryActions.hidden = true;
    feedback('', null);
    return;
  }

  const clozeText = (row.cloze || row.english || '').replace('[BLANK]', '______');
  el.qImg.src = assetPath(row.question_image);
  el.guide.textContent = '';
  el.hintCloze.textContent = clozeText;
  el.aEn.textContent = row.english || '';
  el.aIpa.textContent = row.ipa_us || '';
  el.aJp.textContent = displayJapanese(row);
  el.answerBox.hidden = true;
  el.memoryActions.hidden = true;
  state.hintClozeVisible = false;
  el.hintCloze.hidden = true;
  el.btnHintCloze.textContent = '穴埋めヒント';
  feedback('', null);

  el.audioPlayer.pause();
  el.audioPlayer.src = assetPath(row.audio_file);
  el.audioPlayer.currentTime = 0;
  el.audioPlayer.playbackRate = state.playbackRate;
  el.playbackRate.value = String(state.playbackRate);
}

function showAnswer() {
  const row = currentRow();
  if (!row) return;
  el.answerBox.hidden = false;
  el.memoryActions.hidden = false;
  feedback(`A. ${row.english}`);
}

function nextQ() {
  const rows = activeRows();
  if (!rows.length) {
    render();
    return;
  }
  state.p += 1;
  if (state.p >= rows.length) state.p = 0;
  render();
}

function markMemory(status) {
  const row = currentRow();
  if (!row) return;
  if (status) {
    state.statuses[rowKey(row)] = status;
  } else {
    delete state.statuses[rowKey(row)];
  }
  saveStatuses();
  const rows = activeRows();
  if (!rows.length) {
    state.p = 0;
  } else if (state.p >= rows.length) {
    state.p = 0;
  }
  nextQ();
}

function toggleHintCloze() {
  state.hintClozeVisible = !state.hintClozeVisible;
  el.hintCloze.hidden = !state.hintClozeVisible;
  el.btnHintCloze.textContent = state.hintClozeVisible ? '穴埋めヒントを隠す' : '穴埋めヒント';
}

async function setScope(scope) {
  state.scope = scope === 'must' || scope === 'random' ? scope : 'all';
  state.p = 0;
  saveScope();
  if (state.scope === 'random') {
    state.rows = shuffleRows(await ensureAllRows());
  } else {
    state.rows = await ensureUnitRows(state.unit);
  }
  syncUnitButtons();
  render();
}

function parseInitialUnit() {
  const params = new URLSearchParams(window.location.search);
  const unit = params.get('unit');
  if (unit && UNIT_CONFIG[unit]) return unit;
  const saved = window.localStorage.getItem('eizukan_listening_unit_v1');
  if (saved && UNIT_CONFIG[saved]) return saved;
  return 'U01';
}

function parseInitialScope() {
  const params = new URLSearchParams(window.location.search);
  const scope = params.get('scope');
  if (scope === 'must' || scope === 'all' || scope === 'random') return scope;
  return state.scope;
}

function backToStudy() {
  const url = new URL('./index.html', window.location.href);
  url.searchParams.set('unit', state.unit);
  url.searchParams.set('scope', state.scope);
  window.location.href = url.toString();
}

async function init() {
  renderUnitButtons();
  state.scope = parseInitialScope();
  el.btnScopeAll.addEventListener('click', () => { setScope('all'); });
  el.btnScopeRandom.addEventListener('click', () => { setScope('random'); });
  el.btnScopeMust.addEventListener('click', () => { setScope('must'); });
  el.btnHintCloze.addEventListener('click', toggleHintCloze);
  el.btnCheck.addEventListener('click', showAnswer);
  el.btnNext.addEventListener('click', nextQ);
  el.btnRemembered.addEventListener('click', () => markMemory('remembered'));
  el.btnPending.addEventListener('click', () => markMemory('pending'));
  el.btnUnknown.addEventListener('click', () => markMemory('unknown'));
  el.btnBackToStudy.addEventListener('click', backToStudy);
  el.unitTabs.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-unit]');
    if (!button) return;
    setUnit(button.dataset.unit);
  });
  el.playbackRate.addEventListener('change', () => {
    state.playbackRate = Number(el.playbackRate.value) || 1;
    el.audioPlayer.playbackRate = state.playbackRate;
    savePlaybackRate();
  });

  state.unit = parseInitialUnit();
  syncUnitButtons();
  await setScope(state.scope);
}

init().catch((error) => {
  console.error(error);
  feedback('初期化エラー。consoleを確認してください。', false);
});
