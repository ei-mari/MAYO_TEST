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
  btnImage: document.getElementById('btnImage'),
  btnListening: document.getElementById('btnListening'),
  btnCompose: document.getElementById('btnCompose'),
  btnRadio: document.getElementById('btnRadio'),
  btnList: document.getElementById('btnList'),
  btnReview: document.getElementById('btnReview'),
  btnReviewImageMode: document.getElementById('btnReviewImageMode'),
  btnReviewListeningMode: document.getElementById('btnReviewListeningMode'),
  btnReviewComposeMode: document.getElementById('btnReviewComposeMode'),

  card: document.querySelector('.card'),
  listPanel: document.getElementById('listPanel'),
  listBottomUnits: document.getElementById('listBottomUnits'),
  reviewPanel: document.getElementById('reviewPanel'),
  radioPanel: document.getElementById('radioPanel'),
  listGrid: document.getElementById('listGrid'),
  listEmpty: document.getElementById('listEmpty'),
  qImg: document.getElementById('qImg'),
  guide: document.getElementById('guide'),
  panelImage: document.getElementById('panelImage'),
  panelListening: document.getElementById('panelListening'),
  panelCompose: document.getElementById('panelCompose'),
  cloze: document.getElementById('cloze'),
  jp: document.getElementById('jp'),
  ansCompose: document.getElementById('ansCompose'),

  btnAudio: document.getElementById('btnAudio'),
  btnCheck: document.getElementById('btnCheck'),
  btnNext: document.getElementById('btnNext'),
  btnHintCloze: document.getElementById('btnHintCloze'),
  btnHintJp: document.getElementById('btnHintJp'),
  hintImageJp: document.getElementById('hintImageJp'),
  hintListeningCloze: document.getElementById('hintListeningCloze'),
  hintListeningJp: document.getElementById('hintListeningJp'),
  radioArtwork: document.getElementById('radioArtwork'),
  radioScopeBadge: document.getElementById('radioScopeBadge'),
  radioStatus: document.getElementById('radioStatus'),
  radioNowEn: document.getElementById('radioNowEn'),
  radioNowJp: document.getElementById('radioNowJp'),
  radioUpNext: document.getElementById('radioUpNext'),
  radioSeek: document.getElementById('radioSeek'),
  radioCurrentTime: document.getElementById('radioCurrentTime'),
  radioDuration: document.getElementById('radioDuration'),
  btnRadioPrev: document.getElementById('btnRadioPrev'),
  btnRadioPlay: document.getElementById('btnRadioPlay'),
  btnRadioNext: document.getElementById('btnRadioNext'),
  radioPlaylist: document.getElementById('radioPlaylist'),

  fb: document.getElementById('fb'),
  answerBox: document.getElementById('answerBox'),
  btnRevealIpa: document.getElementById('btnRevealIpa'),
  btnRevealJp: document.getElementById('btnRevealJp'),
  memoryActions: document.getElementById('memoryActions'),
  btnRemembered: document.getElementById('btnRemembered'),
  btnPending: document.getElementById('btnPending'),
  btnUnknown: document.getElementById('btnUnknown'),
  jpAnswer: document.getElementById('jpAnswer'),
  aEn: document.getElementById('aEn'),
  aJp: document.getElementById('aJp'),
  aIpa: document.getElementById('aIpa'),
  audioPlayer: document.getElementById('audioPlayer'),
};

const state = {
  unit: 'U01',
  mode: 'image',
  reviewStudyMode: '',
  scope: loadScope(),
  rows: [],
  p: 0,
  imageHintVisible: false,
  listeningClozeVisible: false,
  listeningJpVisible: false,
  cache: {},
  statuses: loadStatuses(),
  listOpen: {},
  listIpaOpen: {},
  radioPlaying: false,
  radioStarted: false,
  radioWaitingGap: false,
  radioGapTimer: null,
};

function renderUnitButtons() {
  const markup = Object.entries(UNIT_CONFIG)
    .map(([unit, config]) => `<button type="button" data-unit="${escapeHtml(unit)}">${escapeHtml(config.label)}</button>`)
    .join('');
  el.unitTabs.innerHTML = markup;
  el.listBottomUnits.innerHTML = markup;
}

function shuffleRows(rows) {
  const copy = [...rows];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function normalize(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/[.,!?;:'"-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

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
    const saved = JSON.parse(window.localStorage.getItem('eizukan_statuses_v1') || '{}');
    if (saved && typeof saved === 'object' && Object.keys(saved).length > 0) {
      return saved;
    }

    const stars = JSON.parse(window.localStorage.getItem('eizukan_stars_v1') || '{}');
    const migrated = {};
    Object.keys(stars || {}).forEach((key) => {
      if (stars[key]) migrated[key] = 'pending';
    });
    return migrated;
  } catch {
    return {};
  }
}

function loadScope() {
  try {
    const saved = window.localStorage.getItem('eizukan_scope_v1');
    return saved === 'must' || saved === 'random' ? saved : 'all';
  } catch {
    return 'all';
  }
}

function parseInitialUnit() {
  const params = new URLSearchParams(window.location.search);
  const unit = params.get('unit');
  return unit && UNIT_CONFIG[unit] ? unit : 'U01';
}

function parseInitialScope() {
  const params = new URLSearchParams(window.location.search);
  const scope = params.get('scope');
  return scope === 'must' || scope === 'all' || scope === 'random' ? scope : state.scope;
}

function saveScope() {
  window.localStorage.setItem('eizukan_scope_v1', state.scope);
}

function syncUnitButtons() {
  const activeUnit = state.scope === 'random' ? '' : state.unit;
  [...el.unitTabs.querySelectorAll('button[data-unit]')].forEach((button) => {
    button.classList.toggle('active', button.dataset.unit === activeUnit);
  });
  [...el.listBottomUnits.querySelectorAll('button[data-unit]')].forEach((button) => {
    button.classList.toggle('active', button.dataset.unit === activeUnit);
  });
}

function saveStatuses() {
  window.localStorage.setItem('eizukan_statuses_v1', JSON.stringify(state.statuses));
}

function statusModeForView(viewMode = state.mode) {
  if (viewMode === 'review') return state.reviewStudyMode || 'image';
  if (viewMode === 'listening') return 'listening';
  if (viewMode === 'radio') return 'listening';
  return viewMode === 'compose' ? 'compose' : 'image';
}

function statusKey(row, mode = statusModeForView()) {
  return `${mode}:${rowKey(row)}`;
}

function rowKey(row) {
  return `${row.chapter || state.unit}:${row.qno}`;
}

function statusOf(row, mode = statusModeForView()) {
  const namespaced = state.statuses[statusKey(row, mode)];
  if (namespaced) return namespaced;
  if (mode === 'image') {
    return state.statuses[rowKey(row)] || '';
  }
  return '';
}

function isReviewStatus(status) {
  return status === 'pending' || status === 'unknown';
}

function isMustRow(row, mode = statusModeForView()) {
  return statusOf(row, mode) !== 'remembered';
}

function isMustRowAnyMode(row) {
  return isMustRow(row, 'image') || isMustRow(row, 'compose') || isMustRow(row, 'listening');
}

function activeRows() {
  if (state.mode === 'review' && state.reviewStudyMode) {
    return state.rows.filter((row) => isReviewStatus(statusOf(row, state.reviewStudyMode)));
  }
  if (state.scope === 'must') {
    if (state.mode === 'list' || (state.mode === 'review' && !state.reviewStudyMode)) {
      return state.rows.filter(isMustRowAnyMode);
    }
    return state.rows.filter((row) => isMustRow(row));
  }
  return state.rows;
}

function currentRow() {
  const rows = activeRows();
  return rows[state.p];
}

function clampPointer() {
  const rows = activeRows();
  if (!rows.length) {
    state.p = 0;
    return;
  }
  if (state.p >= rows.length) {
    state.p = rows.length - 1;
  }
  if (state.p < 0) {
    state.p = 0;
  }
}

function setStatus(row, status, mode = statusModeForView()) {
  const key = statusKey(row, mode);
  if (!status) {
    delete state.statuses[key];
  } else {
    state.statuses[key] = status;
  }
  saveStatuses();
}

function rowFromKey(key) {
  return state.rows.find((row) => rowKey(row) === key);
}

function escapeHtml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function answersFromRow(r) {
  return (r.accepted || r.phrasal || '')
    .split('|')
    .map((s) => s.trim())
    .filter(Boolean);
}

function displayJapanese(r) {
  return r.japanese || r.english || '';
}

function scopeLabel(scope = state.scope) {
  if (scope === 'must') return 'MUST';
  if (scope === 'random') return 'RANDOM';
  return 'ALL';
}

function formatTime(seconds) {
  const safe = Number.isFinite(seconds) && seconds >= 0 ? seconds : 0;
  const mins = Math.floor(safe / 60);
  const secs = Math.floor(safe % 60);
  return `${mins}:${String(secs).padStart(2, '0')}`;
}

function syncRadioProgress() {
  const duration = Number.isFinite(el.audioPlayer.duration) ? el.audioPlayer.duration : 0;
  const current = Number.isFinite(el.audioPlayer.currentTime) ? el.audioPlayer.currentTime : 0;
  const ratio = duration > 0 ? (current / duration) * 100 : 0;
  el.radioSeek.value = String(ratio);
  el.radioCurrentTime.textContent = formatTime(current);
  el.radioDuration.textContent = formatTime(duration);
}

function resetRadioProgress() {
  el.radioSeek.value = '0';
  el.radioCurrentTime.textContent = '0:00';
  el.radioDuration.textContent = '0:00';
}

function clearRadioAdvanceTimer() {
  if (state.radioGapTimer) {
    window.clearTimeout(state.radioGapTimer);
    state.radioGapTimer = null;
  }
  state.radioWaitingGap = false;
}

function feedback(msg, ok) {
  el.fb.textContent = msg;
  el.fb.classList.remove('ok', 'ng');
  if (ok === true) el.fb.classList.add('ok');
  if (ok === false) el.fb.classList.add('ng');
}

function render() {
  if (state.mode === 'radio') {
    renderRadioMode();
    return;
  }
  if (state.mode === 'list') {
    renderListMode();
    return;
  }
  if (state.mode === 'review' && !state.reviewStudyMode) {
    renderReviewModeChooser();
    return;
  }

  const r = currentRow();
  const studyMode = statusModeForView();
  if (!r) {
    el.card.hidden = false;
    el.listPanel.hidden = true;
    el.reviewPanel.hidden = true;
    el.qImg.removeAttribute('src');
    el.cloze.textContent = '';
    el.jp.textContent = '';
    el.aEn.textContent = '';
    el.aJp.textContent = '';
    el.aIpa.textContent = '';
    el.answerBox.hidden = true;
    el.memoryActions.hidden = true;
    el.fb.textContent = '';
    el.fb.classList.remove('ok', 'ng');
    el.btnAudio.hidden = true;
    el.btnHintCloze.hidden = true;
    el.btnHintJp.hidden = true;
    el.btnCheck.hidden = true;
    el.btnNext.hidden = true;
    el.guide.textContent = state.mode === 'review'
      ? 'このレビューで残っているカードはありません。'
      : state.scope === 'must'
      ? 'MUST に表示できるカードがありません。ALL に切り替えると全問題を表示できます。'
      : '表示できるカードがありません。';
    return;
  }

  const clozeText = (r.cloze || r.english || '').replace('[BLANK]', '<span class="blank">______</span>');
  const listeningMode = studyMode === 'listening';

  el.card.hidden = false;
  el.listPanel.hidden = true;
  el.reviewPanel.hidden = true;
  el.radioPanel.hidden = true;
  el.btnAudio.hidden = false;
  el.btnCheck.hidden = false;
  el.btnNext.hidden = false;
  el.btnHintCloze.hidden = !listeningMode;
  el.btnHintJp.hidden = !(studyMode === 'image' || listeningMode);
  el.qImg.src = assetPath(r.question_image);
  el.cloze.innerHTML = clozeText;
  el.jp.textContent = displayJapanese(r);
  el.aEn.textContent = r.english;
  el.aJp.textContent = displayJapanese(r);
  el.aIpa.textContent = r.ipa_us;
  el.hintImageJp.textContent = displayJapanese(r);
  el.hintListeningCloze.innerHTML = clozeText;
  el.hintListeningJp.textContent = displayJapanese(r);

  el.ansCompose.value = '';
  el.answerBox.hidden = true;
  el.memoryActions.hidden = true;
  el.aIpa.hidden = true;
  el.jpAnswer.hidden = true;
  el.btnRevealIpa.textContent = '発音記号';
  el.btnRevealIpa.setAttribute('aria-expanded', 'false');
  el.btnRevealJp.textContent = '和訳を見る';
  el.btnRevealJp.setAttribute('aria-expanded', 'false');
  el.fb.textContent = '';
  el.fb.classList.remove('ok', 'ng');

  state.imageHintVisible = false;
  state.listeningClozeVisible = false;
  state.listeningJpVisible = false;
  el.hintImageJp.hidden = true;
  el.hintListeningCloze.hidden = true;
  el.hintListeningJp.hidden = true;
  el.btnHintCloze.textContent = '穴埋めヒント';
  el.btnHintCloze.setAttribute('aria-expanded', 'false');
  el.btnHintJp.textContent = studyMode === 'image' ? 'ヒント' : '日本語ヒント';
  el.btnHintJp.setAttribute('aria-expanded', 'false');

  el.guide.textContent = studyMode === 'image'
    ? '画像と文脈を見て頭の中で英文を完成させた後、答えを確認してください。'
    : studyMode === 'listening'
    ? ''
    : '日本語を見て英文を思い出してください。';

  el.audioPlayer.pause();
  el.audioPlayer.currentTime = 0;
  el.audioPlayer.src = assetPath(r.audio_file);

  if (studyMode === 'compose') {
    el.ansCompose.focus();
  }
  if (listeningMode) {
    playAudio(true);
  }
}

function setMode(mode) {
  if (state.mode === 'radio' && mode !== 'radio') {
    pauseRadio();
  }
  if (state.mode !== 'radio' && mode === 'radio') {
    clearRadioAdvanceTimer();
    el.audioPlayer.pause();
    el.audioPlayer.currentTime = 0;
  }
  state.mode = mode;
  if (mode !== 'review') {
    state.reviewStudyMode = '';
  }
  const studyMode = statusModeForView(mode);
  const image = mode === 'image' || (mode === 'review' && state.reviewStudyMode === 'image');
  const listening = mode === 'listening' || (mode === 'review' && state.reviewStudyMode === 'listening');
  const compose = mode === 'compose' || (mode === 'review' && state.reviewStudyMode === 'compose');
  const radio = mode === 'radio';
  const chooser = mode === 'review' && !state.reviewStudyMode;
  const listLike = mode === 'list' || chooser || radio;

  el.btnCheck.textContent = studyMode === 'compose' ? '回答' : '答えを見る';
  el.btnAudio.hidden = listLike;
  el.btnHintCloze.hidden = studyMode !== 'listening' || listLike;
  el.btnHintJp.hidden = !(studyMode === 'image' || studyMode === 'listening') || listLike;
  el.btnCheck.hidden = listLike;
  el.btnNext.hidden = listLike;
  el.fb.hidden = listLike;
  el.answerBox.hidden = true;
  el.btnImage.classList.toggle('active', image);
  el.btnListening.classList.toggle('active', listening);
  el.btnCompose.classList.toggle('active', compose);
  el.btnRadio.classList.toggle('active', radio);
  el.btnList.classList.toggle('active', mode === 'list');
  el.btnReview.classList.toggle('active', mode === 'review');
  el.btnScopeAll.classList.toggle('active', state.scope === 'all');
  el.btnScopeRandom.classList.toggle('active', state.scope === 'random');
  el.btnScopeMust.classList.toggle('active', state.scope === 'must');
  el.panelImage.classList.toggle('active', image);
  el.panelListening.classList.toggle('active', listening);
  el.panelCompose.classList.toggle('active', compose);
  el.radioPanel.hidden = !radio;
  syncUnitButtons();

  render();
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
  clampPointer();
  render();
}

function startReview(studyMode) {
  state.mode = 'review';
  state.reviewStudyMode = studyMode === 'compose'
    ? 'compose'
    : studyMode === 'listening'
    ? 'listening'
    : 'image';
  state.p = 0;
  render();
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

async function setUnit(unit) {
  state.unit = unit;
  syncUnitButtons();
  if (state.scope !== 'random') {
    state.rows = await ensureUnitRows(unit);
  }
  state.p = 0;
  state.listOpen = {};
  clampPointer();
  render();
}

function answerLabel(r) {
  const answers = answersFromRow(r);
  if (statusModeForView() === 'image') {
    return r.phrasal || answers[0] || '';
  }
  return r.english || '';
}

function showAnswer() {
  const r = currentRow();
  if (!r) return;
  el.answerBox.hidden = false;
  el.memoryActions.hidden = false;
  el.aIpa.hidden = true;
  el.btnRevealIpa.textContent = '発音記号';
  el.btnRevealIpa.setAttribute('aria-expanded', 'false');
  feedback(`A. ${answerLabel(r)}`);
  playAudio(true);
}

function toggleAnswerIpa() {
  if (el.answerBox.hidden) return;
  const visible = el.aIpa.hidden;
  el.aIpa.hidden = !visible;
  el.btnRevealIpa.textContent = visible ? '発音記号を隠す' : '発音記号';
  el.btnRevealIpa.setAttribute('aria-expanded', String(visible));
}

function toggleAnswerJp() {
  if (el.answerBox.hidden) return;
  const visible = el.jpAnswer.hidden;
  el.jpAnswer.hidden = !visible;
  el.btnRevealJp.textContent = visible ? '和訳を隠す' : '和訳を見る';
  el.btnRevealJp.setAttribute('aria-expanded', String(visible));
}

function toggleHintJp() {
  const studyMode = statusModeForView();
  if (!currentRow() || (studyMode !== 'image' && studyMode !== 'listening')) return;
  if (studyMode === 'image') {
    state.imageHintVisible = !state.imageHintVisible;
    el.hintImageJp.hidden = !state.imageHintVisible;
    el.btnHintJp.textContent = state.imageHintVisible ? 'ヒントを隠す' : 'ヒント';
    el.btnHintJp.setAttribute('aria-expanded', String(state.imageHintVisible));
    return;
  }
  state.listeningJpVisible = !state.listeningJpVisible;
  el.hintListeningJp.hidden = !state.listeningJpVisible;
  el.btnHintJp.textContent = state.listeningJpVisible ? '日本語ヒントを隠す' : '日本語ヒント';
  el.btnHintJp.setAttribute('aria-expanded', String(state.listeningJpVisible));
}

function toggleHintCloze() {
  if (!currentRow() || statusModeForView() !== 'listening') return;
  state.listeningClozeVisible = !state.listeningClozeVisible;
  el.hintListeningCloze.hidden = !state.listeningClozeVisible;
  el.btnHintCloze.textContent = state.listeningClozeVisible ? '穴埋めヒントを隠す' : '穴埋めヒント';
  el.btnHintCloze.setAttribute('aria-expanded', String(state.listeningClozeVisible));
}

function playRowAudio(row, silent = false) {
  if (!row || !row.audio_file) {
    if (!silent) feedback('音声がありません。', false);
    return Promise.resolve(false);
  }

  const nextSrc = assetPath(row.audio_file);
  if (!el.audioPlayer.src || !el.audioPlayer.src.endsWith(row.audio_file)) {
    el.audioPlayer.src = nextSrc;
  }

  el.audioPlayer.currentTime = 0;
  updateMediaSession(row);
  return el.audioPlayer.play()
    .then(() => {
      if (!silent) feedback('音声を再生中', true);
      return true;
    })
    .catch(() => {
      if (!silent) feedback('音声を再生できませんでした。', false);
      return false;
    });
}

function playAudio(silent = false) {
  playRowAudio(currentRow(), silent);
}

function radioRows() {
  return activeRows();
}

function radioStatusText() {
  const rows = radioRows();
  const row = currentRow();
  if (!rows.length) return '再生できる音声がありません。';
  if (!row) return '再生待ちです。';
  const prefix = `${state.p + 1} / ${rows.length}`;
  if (state.radioWaitingGap) return `${prefix} を 3 秒後に再生します`;
  if (state.radioPlaying) return `${prefix} を再生中`;
  if (state.radioStarted) return `${prefix} で一時停止中`;
  return `${prefix} から再生できます`;
}

function renderRadioMode() {
  clampPointer();
  el.card.hidden = true;
  el.listPanel.hidden = true;
  el.reviewPanel.hidden = true;
  el.radioPanel.hidden = false;
  el.guide.textContent = '';
  el.fb.textContent = '';
  el.fb.classList.remove('ok', 'ng');
  el.answerBox.hidden = true;

  const rows = radioRows();
  const row = currentRow();
  const nextRow = rows[state.p + 1] || null;

  el.radioArtwork.src = row ? assetPath(row.question_image) : '';
  el.radioArtwork.hidden = !row;
  el.radioScopeBadge.textContent = scopeLabel();
  el.radioStatus.textContent = radioStatusText();
  el.radioNowEn.textContent = row ? row.english : '音声を流すと英文がここに表示されます。';
  el.radioNowJp.textContent = row ? displayJapanese(row) : '和訳もここに表示されます。';
  el.radioUpNext.textContent = nextRow
    ? `Up next: ${nextRow.english}`
    : rows.length
    ? 'このトラックでキューの最後です。'
    : '次のトラックはここに表示されます。';
  el.btnRadioPlay.textContent = state.radioPlaying ? '一時停止' : state.radioWaitingGap ? '今すぐ再生' : '再生';
  el.btnRadioPlay.disabled = rows.length === 0;
  el.btnRadioPrev.disabled = rows.length === 0;
  el.btnRadioNext.disabled = rows.length === 0;
  el.radioSeek.disabled = rows.length === 0;
  syncRadioProgress();

  el.radioPlaylist.innerHTML = rows.map((candidate, index) => `
    <article class="radioItem">
      <button
        type="button"
        class="radioItemButton ${index === state.p ? 'active' : ''}"
        data-action="pick-radio-row"
        data-index="${index}"
      >
        <div class="radioItemTop">
          <span class="radioItemNo">TRACK ${index + 1}</span>
          <span class="radioItemState">${index === state.p ? (state.radioPlaying ? 'NOW PLAYING' : 'CURRENT') : ''}</span>
        </div>
        <div class="radioItemBody">
          <img class="radioItemArtwork" src="${escapeHtml(assetPath(candidate.question_image))}" alt="">
          <div class="radioItemText">
            <p class="radioItemEn">${escapeHtml(candidate.english)}</p>
            <p class="radioItemJp">${escapeHtml(displayJapanese(candidate))}</p>
          </div>
        </div>
      </button>
    </article>
  `).join('');
}

function pauseRadio() {
  clearRadioAdvanceTimer();
  state.radioPlaying = false;
  el.audioPlayer.pause();
  updateMediaSessionPlaybackState();
  if (state.mode === 'radio') renderRadioMode();
}

async function startRadioPlayback() {
  const row = currentRow();
  if (!row) {
    renderRadioMode();
    return;
  }
  clearRadioAdvanceTimer();
  state.radioStarted = true;
  const ok = await playRowAudio(row, true);
  state.radioPlaying = ok;
  updateMediaSessionPlaybackState();
  if (state.mode === 'radio') renderRadioMode();
}

function toggleRadioPlayback() {
  if (state.radioPlaying) {
    pauseRadio();
    return;
  }
  if (state.radioWaitingGap) {
    startRadioPlayback();
    return;
  }
  startRadioPlayback();
}

function seekRadio(event) {
  const ratio = Number.parseFloat(event.target.value || '0');
  if (!Number.isFinite(ratio)) return;
  const duration = Number.isFinite(el.audioPlayer.duration) ? el.audioPlayer.duration : 0;
  if (duration <= 0) return;
  el.audioPlayer.currentTime = (ratio / 100) * duration;
  syncRadioProgress();
}

function moveRadio(delta, autoplay = state.radioPlaying || state.radioStarted) {
  const rows = radioRows();
  if (!rows.length) {
    renderRadioMode();
    return;
  }
  clearRadioAdvanceTimer();
  state.p = (state.p + delta + rows.length) % rows.length;
  if (autoplay) {
    startRadioPlayback();
    return;
  }
  renderRadioMode();
}

function handleRadioEnded() {
  if (state.mode !== 'radio' || !state.radioPlaying) return;
  const rows = radioRows();
  if (!rows.length) {
    pauseRadio();
    return;
  }
  if (state.p >= rows.length - 1) {
    state.radioPlaying = false;
    updateMediaSessionPlaybackState();
    renderRadioMode();
    return;
  }
  state.p += 1;
  state.radioPlaying = false;
  state.radioWaitingGap = true;
  resetRadioProgress();
  updateMediaSessionPlaybackState();
  renderRadioMode();
  state.radioGapTimer = window.setTimeout(() => {
    state.radioGapTimer = null;
    if (state.mode !== 'radio') return;
    startRadioPlayback();
  }, 3000);
}

function handleRadioPlaylistClick(event) {
  const button = event.target.closest('button[data-action="pick-radio-row"]');
  if (!button) return;
  const index = Number.parseInt(button.dataset.index || '', 10);
  if (!Number.isInteger(index)) return;
  clearRadioAdvanceTimer();
  state.p = index;
  startRadioPlayback();
}

function updateMediaSession(row) {
  if (!('mediaSession' in navigator)) return;
  navigator.mediaSession.metadata = new MediaMetadata({
    title: row?.english || 'Eijukugo Radio',
    artist: row?.chapter || UNIT_CONFIG[state.unit]?.label || 'Eijukugo Zukan',
    album: 'Radio Mode',
  });
}

function updateMediaSessionPlaybackState() {
  if (!('mediaSession' in navigator)) return;
  navigator.mediaSession.playbackState = state.radioPlaying ? 'playing' : 'paused';
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

  setStatus(row, status);
  const afterRows = activeRows();
  const currentKey = rowKey(row);

  if (!afterRows.length) {
    state.p = 0;
    render();
    return;
  }

  const stillVisible = afterRows.some((candidate) => rowKey(candidate) === currentKey);
  if (stillVisible) {
    state.p = (Math.min(state.p, afterRows.length - 1) + 1) % afterRows.length;
  } else {
    state.p = Math.min(state.p, afterRows.length - 1);
  }
  render();
}

function listRows() {
  return activeRows();
}

function statusButtons(key, currentStatus, modeLabel, modeKey) {
  return `
    <div class="statusGroup" data-status-mode="${escapeHtml(modeKey)}">
      <p class="statusGroupLabel">${escapeHtml(modeLabel)}</p>
      <div class="statusPicker">
      <button type="button" class="statusOption remembered ${currentStatus === 'remembered' ? 'active' : ''}" data-action="set-status" data-key="${escapeHtml(key)}" data-status="remembered">覚えた</button>
      <button type="button" class="statusOption pending ${currentStatus === 'pending' ? 'active' : ''}" data-action="set-status" data-key="${escapeHtml(key)}" data-status="pending">保留</button>
      <button type="button" class="statusOption unknown ${currentStatus === 'unknown' ? 'active' : ''}" data-action="set-status" data-key="${escapeHtml(key)}" data-status="unknown">覚えてない</button>
      </div>
    </div>
  `;
}

function renderListMode() {
  el.card.hidden = true;
  el.listPanel.hidden = false;
  el.reviewPanel.hidden = true;
  el.radioPanel.hidden = true;
  el.guide.textContent = '';
  el.fb.textContent = '';
  el.fb.classList.remove('ok', 'ng');
  el.answerBox.hidden = true;

  const rows = listRows();
  el.listEmpty.textContent = state.mode === 'review'
    ? 'まだ保留 / 覚えてない問題がありません。'
    : '表示できるカードがありません。';
  el.listEmpty.hidden = rows.length > 0;
  [...el.listBottomUnits.querySelectorAll('button')].forEach((button) => {
    button.classList.toggle('active', button.dataset.unit === state.unit);
  });
  el.listGrid.innerHTML = rows.map((row) => {
    const key = rowKey(row);
    const open = Boolean(state.listOpen[key]);
    const imageStatus = statusOf(row, 'image');
    const composeStatus = statusOf(row, 'compose');
    const ipaOpen = Boolean(state.listIpaOpen[key]);

    return `
      <article class="listCard" data-key="${escapeHtml(key)}">
        <div class="listMain">
          <img class="listCardImage" src="${escapeHtml(assetPath(row.question_image))}" alt="">
        </div>
        <div class="listBody">
          <p class="listJp">${escapeHtml(displayJapanese(row))}</p>
          <div class="listMeta">
            <span class="listMetaText">タップで答えを見る</span>
          </div>
          ${statusButtons(key, imageStatus, '穴埋め', 'image')}
          ${statusButtons(key, statusOf(row, 'listening'), 'リスニング', 'listening')}
          ${statusButtons(key, composeStatus, '瞬間英作文', 'compose')}
        </div>
        <div class="listAnswer" ${open ? '' : 'hidden'}>
          <div class="listAnswerInner">
            <p>${escapeHtml(row.english)}</p>
            <div class="listAnswerTools">
              <button type="button" class="ghostChip" data-action="toggle-ipa" data-key="${escapeHtml(key)}">${ipaOpen ? '発音記号を隠す' : '発音記号'}</button>
              <button type="button" class="ghostChip" data-action="play-audio" data-key="${escapeHtml(key)}">🎧</button>
            </div>
            <p ${ipaOpen ? '' : 'hidden'}>${escapeHtml(row.ipa_us)}</p>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

function renderReviewModeChooser() {
  el.card.hidden = true;
  el.listPanel.hidden = true;
  el.reviewPanel.hidden = false;
  el.radioPanel.hidden = true;
  el.answerBox.hidden = true;
  el.fb.textContent = '';
  el.fb.classList.remove('ok', 'ng');
  el.guide.textContent = '';
}

function handleListClick(event) {
  const button = event.target.closest('button');
  if (!button) {
    const card = event.target.closest('.listCard');
    if (!card) return;
    const key = card.dataset.key;
    if (!key) return;
    state.listOpen[key] = !state.listOpen[key];
    renderListMode();
    return;
  }

  const action = button.dataset.action;
  const key = button.dataset.key;
  if (!action || !key) return;

  const row = rowFromKey(key);
  if (!row) return;

  if (action === 'toggle-answer') {
    state.listOpen[key] = !state.listOpen[key];
    renderListMode();
    return;
  }

  if (action === 'set-status') {
    const status = button.dataset.status || '';
    const mode = button.closest('.statusGroup')?.dataset.statusMode || 'image';
    setStatus(row, status, mode);
    renderListMode();
    return;
  }

  if (action === 'toggle-ipa') {
    state.listIpaOpen[key] = !state.listIpaOpen[key];
    renderListMode();
    return;
  }

  if (action === 'play-audio') {
    playRowAudio(row, true);
  }
}

async function init() {
  renderUnitButtons();
  state.scope = parseInitialScope();
  el.btnImage.addEventListener('click', () => setMode('image'));
  el.btnListening.addEventListener('click', () => {
    const url = new URL('./listening.html', window.location.href);
    url.searchParams.set('unit', state.unit);
    url.searchParams.set('scope', state.scope);
    window.location.href = url.toString();
  });
  el.btnCompose.addEventListener('click', () => setMode('compose'));
  el.btnRadio.addEventListener('click', () => setMode('radio'));
  el.btnList.addEventListener('click', () => setMode('list'));
  el.btnReview.addEventListener('click', () => setMode('review'));
  el.btnReviewImageMode.addEventListener('click', () => startReview('image'));
  el.btnReviewListeningMode.addEventListener('click', () => startReview('listening'));
  el.btnReviewComposeMode.addEventListener('click', () => startReview('compose'));
  el.btnScopeAll.addEventListener('click', () => { setScope('all'); });
  el.btnScopeRandom.addEventListener('click', () => { setScope('random'); });
  el.btnScopeMust.addEventListener('click', () => { setScope('must'); });
  el.btnAudio.addEventListener('click', playAudio);
  el.btnCheck.addEventListener('click', showAnswer);
  el.btnNext.addEventListener('click', nextQ);
  el.btnHintCloze.addEventListener('click', toggleHintCloze);
  el.btnHintJp.addEventListener('click', toggleHintJp);
  el.btnRevealIpa.addEventListener('click', toggleAnswerIpa);
  el.btnRevealJp.addEventListener('click', toggleAnswerJp);
  el.btnRemembered.addEventListener('click', () => markMemory('remembered'));
  el.btnPending.addEventListener('click', () => markMemory('pending'));
  el.btnUnknown.addEventListener('click', () => markMemory('unknown'));
  el.btnRadioPrev.addEventListener('click', () => moveRadio(-1));
  el.btnRadioPlay.addEventListener('click', toggleRadioPlayback);
  el.btnRadioNext.addEventListener('click', () => moveRadio(1));
  el.radioSeek.addEventListener('input', seekRadio);
  el.radioPlaylist.addEventListener('click', handleRadioPlaylistClick);
  el.listGrid.addEventListener('click', handleListClick);
  el.audioPlayer.addEventListener('ended', handleRadioEnded);
  el.audioPlayer.addEventListener('pause', () => {
    updateMediaSessionPlaybackState();
    if (state.mode === 'radio') renderRadioMode();
  });
  el.audioPlayer.addEventListener('play', () => {
    updateMediaSessionPlaybackState();
    syncRadioProgress();
    if (state.mode === 'radio') renderRadioMode();
  });
  el.audioPlayer.addEventListener('timeupdate', syncRadioProgress);
  el.audioPlayer.addEventListener('loadedmetadata', syncRadioProgress);
  el.listBottomUnits.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-unit]');
    if (!button) return;
    setUnit(button.dataset.unit);
  });
  el.unitTabs.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-unit]');
    if (!button) return;
    setUnit(button.dataset.unit);
  });

  el.ansCompose.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      showAnswer();
    }
  });

  if ('mediaSession' in navigator) {
    navigator.mediaSession.setActionHandler('play', startRadioPlayback);
    navigator.mediaSession.setActionHandler('pause', pauseRadio);
    navigator.mediaSession.setActionHandler('previoustrack', () => moveRadio(-1));
    navigator.mediaSession.setActionHandler('nexttrack', () => moveRadio(1));
  }

  setMode('image');
  state.unit = parseInitialUnit();
  syncUnitButtons();
  await setScope(state.scope);
}

init().catch((e) => {
  console.error(e);
  feedback('初期化エラー。consoleを確認してください。', false);
});
