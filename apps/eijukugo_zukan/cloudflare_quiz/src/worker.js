const jsonHeaders = {
  'content-type': 'application/json; charset=utf-8',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'access-control-allow-origin': '*',
          'access-control-allow-methods': 'GET,POST,OPTIONS',
          'access-control-allow-headers': 'content-type',
        },
      });
    }

    if (url.pathname === '/api/health') {
      return Response.json({
        ok: true,
        app: env.APP_NAME || 'Phrasal Verb Training',
      });
    }

    if (url.pathname === '/api/submissions' && request.method === 'POST') {
      return handleSubmission(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};

async function handleSubmission(request, env) {
  if (!env.DB) {
    return json({ error: 'missing_d1_binding' }, 500);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'invalid_json' }, 400);
  }

  const payload = normalizePayload(body, request);
  if (!payload.ok) {
    return json({ error: payload.error }, 400);
  }

  const data = payload.data;

  try {
    const result = await env.DB.prepare(
      `INSERT INTO submissions (
        learner_id,
        unit,
        qno,
        mode,
        prompt_japanese,
        correct_answer,
        user_answer,
        ipa_us,
        source_audio,
        source_image,
        user_agent,
        client_timestamp
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
      .bind(
        data.learnerId,
        data.unit,
        data.qno,
        data.mode,
        data.promptJapanese,
        data.correctAnswer,
        data.userAnswer,
        data.ipaUs,
        data.sourceAudio,
        data.sourceImage,
        data.userAgent,
        data.clientTimestamp
      )
      .run();

    await notifySlack(env, data, result.meta?.last_row_id);

    return json({
      ok: true,
      id: result.meta?.last_row_id || null,
    });
  } catch (error) {
    console.error('submission_failed', error);
    return json({ error: 'submission_failed' }, 500);
  }
}

function normalizePayload(body, request) {
  const data = {
    learnerId: text(body.learnerId, 128),
    unit: text(body.unit, 16),
    qno: toPositiveInt(body.qno),
    mode: text(body.mode, 16),
    promptJapanese: text(body.promptJapanese, 500),
    correctAnswer: text(body.correctAnswer, 500),
    userAnswer: text(body.userAnswer, 1000),
    ipaUs: text(body.ipaUs, 500),
    sourceAudio: text(body.sourceAudio, 500),
    sourceImage: text(body.sourceImage, 500),
    clientTimestamp: text(body.clientTimestamp, 64),
    userAgent: text(request.headers.get('user-agent'), 500),
  };

  if (!data.unit) return { ok: false, error: 'unit_required' };
  if (!data.qno) return { ok: false, error: 'qno_required' };
  if (!['compose', 'image'].includes(data.mode)) return { ok: false, error: 'mode_invalid' };
  if (!data.promptJapanese) return { ok: false, error: 'prompt_required' };
  if (!data.correctAnswer) return { ok: false, error: 'correct_answer_required' };
  if (!data.userAnswer) return { ok: false, error: 'user_answer_required' };

  return { ok: true, data };
}

async function notifySlack(env, data, rowId) {
  if (!env.SLACK_WEBHOOK_URL) return;

  const lines = [
    `*${env.APP_NAME || 'Phrasal Verb Training'}* に提出がありました`,
    `ID: ${rowId || '-'}`,
    `UNIT: ${data.unit} / Q${data.qno}`,
    `Mode: ${data.mode}`,
    `JP: ${data.promptJapanese}`,
    `User: ${data.userAnswer}`,
    `Answer: ${data.correctAnswer}`,
  ];

  const res = await fetch(env.SLACK_WEBHOOK_URL, {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({
      text: lines.join('\n'),
    }),
  });

  if (!res.ok) {
    const message = await res.text();
    console.error('slack_notify_failed', message);
  }
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: jsonHeaders,
  });
}

function text(value, maxLen) {
  return String(value || '').trim().slice(0, maxLen);
}

function toPositiveInt(value) {
  const num = Number.parseInt(String(value || ''), 10);
  return Number.isFinite(num) && num > 0 ? num : 0;
}
