const SPLITS = ['dev', 'test', 'fresh_hard'];
const OPTION_KEYS = ['A', 'B', 'C', 'D', 'E', 'F'];
const KNOWLEDGE_TYPES = new Set([
  'fact',
  'parameter',
  'condition',
  'method',
  'mechanism',
  'comparison',
  'synthesis'
]);
const DIFFICULTIES = new Set(['easy', 'medium', 'hard']);

const DEFAULTS = {
  subdomain: 'general',
  knowledge_type: 'fact',
  difficulty: 'medium',
  quality_score: 1.0
};

export function buildDomainRAGBundle(evalItems, options = {}) {
  const rows = Array.isArray(evalItems) ? evalItems : [];
  const prepared = [];
  const skipped = [];

  for (const item of rows) {
    const result = normalizeEvalItem(item, options);
    if (result.error) {
      skipped.push({ id: item && item.id ? item.id : null, reason: result.error });
    } else {
      prepared.push(result.item);
    }
  }

  assignFallbackSplits(prepared);
  const errors = validateBundle(prepared);
  if (errors.length > 0) {
    return { files: [], statistics: buildStatistics(prepared), skipped, errors };
  }

  const chunks = buildChunkRecords(prepared);
  return {
    files: [
      { path: 'chunks.jsonl', content: toJsonl(chunks) },
      { path: 'items.jsonl', content: toJsonl(prepared.map(entry => entry.domainragItem)) }
    ],
    statistics: buildStatistics(prepared),
    skipped,
    errors: []
  };
}

function normalizeEvalItem(item, options) {
  if (!item || typeof item !== 'object') {
    return { error: 'item must be an object' };
  }
  if (!item.id) {
    return { error: 'item id is required' };
  }
  if (!item.question) {
    return { error: 'question is required' };
  }

  const chunk = item.chunks || item.chunk || null;
  const chunkId = item.chunkId || (chunk && chunk.id);
  if (!chunkId) {
    return { error: 'chunkId is required for DomainRAG qrels' };
  }
  if (!chunk || !chunk.content || !String(chunk.content).trim()) {
    return { error: 'included chunk content is required' };
  }

  const questionType = normalizeQuestionType(item.questionType || item.question_type);
  if (!questionType) {
    return { error: `unsupported question type: ${item.questionType || item.question_type || 'unknown'}` };
  }

  const optionResult = normalizeOptions(item.options, questionType);
  if (optionResult.error) {
    return { error: optionResult.error };
  }

  const answerResult = normalizeAnswer(item.correctAnswer ?? item.answer, questionType);
  if (answerResult.error) {
    return { error: answerResult.error };
  }

  const tags = extractTags(item.tags);
  const split = resolveSplit(item, tags, options);
  const override = itemOverride(item.id, options);
  const defaults = { ...DEFAULTS, ...(options.defaults || {}) };

  const referenceAnswer = String(
    override.reference_answer ||
      item.referenceAnswer ||
      item.reference_answer ||
      answerResult.answer.join(', ')
  );
  const answerAliases = toArray(override.answer_aliases || defaults.answer_aliases || []);
  const requiredPoints = toArray(
    override.required_points ||
      defaults.required_points ||
      (questionType === 'short_answer' ? [referenceAnswer] : [])
  );

  if (questionType === 'fill_blank' && answerAliases.length === 0) {
    answerAliases.push(...answerResult.answer);
  }
  if (questionType === 'short_answer' && requiredPoints.length === 0) {
    requiredPoints.push(referenceAnswer);
  }

  const knowledgeType = resolveEnumValue(
    override.knowledge_type,
    extractTagValue(tags, ['knowledge_type', 'knowledge']),
    defaults.knowledge_type,
    KNOWLEDGE_TYPES,
    DEFAULTS.knowledge_type
  );
  const difficulty = resolveEnumValue(
    override.difficulty,
    extractTagValue(tags, ['difficulty']),
    defaults.difficulty,
    DIFFICULTIES,
    DEFAULTS.difficulty
  );

  const subdomain =
    override.subdomain ||
    extractTagValue(tags, ['subdomain', 'domain']) ||
    defaults.subdomain ||
    DEFAULTS.subdomain;
  const qualityScore = resolveQualityScore(
    override.quality_score,
    extractTagValue(tags, ['quality_score', 'quality']),
    defaults.quality_score
  );

  return {
    item: {
      chunk: {
        id: String(chunkId),
        name: chunk.name || String(chunkId),
        fileName: chunk.fileName || '',
        content: String(chunk.content)
      },
      domainragItem: {
        id: String(item.id),
        split,
        question_type: questionType,
        question: String(item.question),
        options: optionResult.options,
        answer: answerResult.answer,
        answer_aliases: answerAliases,
        reference_answer: referenceAnswer,
        required_points: requiredPoints,
        source_chunk_ids: [String(chunkId)],
        subdomain: String(subdomain),
        knowledge_type: knowledgeType,
        difficulty,
        quality_score: qualityScore
      }
    }
  };
}

function normalizeQuestionType(value) {
  const questionType = String(value || '').trim();
  if (questionType === 'single_choice') return 'single_choice';
  if (questionType === 'multiple_choice') return 'multiple_choice';
  if (questionType === 'short_answer') return 'short_answer';
  if (questionType === 'open_ended') return 'short_answer';
  if (questionType === 'fill_blank') return 'fill_blank';
  return null;
}

function normalizeOptions(rawOptions, questionType) {
  if (!['single_choice', 'multiple_choice'].includes(questionType)) {
    return { options: {} };
  }

  const parsed = parseMaybeJson(rawOptions);
  let options = {};
  if (Array.isArray(parsed)) {
    options = Object.fromEntries(parsed.map((value, index) => [OPTION_KEYS[index], String(value)]));
  } else if (parsed && typeof parsed === 'object') {
    options = Object.fromEntries(
      Object.entries(parsed).map(([key, value], index) => [
        OPTION_KEYS.includes(String(key).toUpperCase()) ? String(key).toUpperCase() : OPTION_KEYS[index],
        String(value)
      ])
    );
  }

  const optionKeys = Object.keys(options).sort();
  if (questionType === 'single_choice' && optionKeys.join('') !== 'ABCD') {
    return { error: 'single_choice requires exactly four A-D options' };
  }
  if (
    questionType === 'multiple_choice' &&
    optionKeys.join('') !== 'ABCDE' &&
    optionKeys.join('') !== 'ABCDEF'
  ) {
    return { error: 'multiple_choice requires five or six A-F options' };
  }
  if (Object.values(options).some(value => !String(value).trim())) {
    return { error: `${questionType} options must be non-empty strings` };
  }
  return { options };
}

function normalizeAnswer(rawAnswer, questionType) {
  const parsed = parseMaybeJson(rawAnswer);
  let answer = toArray(parsed).map(value => String(value).trim()).filter(Boolean);

  if (['single_choice', 'multiple_choice'].includes(questionType)) {
    answer = answer.map(normalizeChoiceAnswer).filter(Boolean);
  }

  if (answer.length === 0) {
    return { error: 'answer is required' };
  }
  if (questionType === 'single_choice' && answer.length !== 1) {
    return { error: 'single_choice requires exactly one answer' };
  }
  if (questionType === 'multiple_choice' && new Set(answer).size < 2) {
    return { error: 'multiple_choice requires at least two distinct answers' };
  }

  return { answer: [...new Set(answer)] };
}

function normalizeChoiceAnswer(value) {
  const answer = String(value).trim().toUpperCase();
  if (OPTION_KEYS.includes(answer)) {
    return answer;
  }
  if (/^[0-5]$/.test(answer)) {
    return OPTION_KEYS[Number(answer)];
  }
  return answer;
}

function extractTags(rawTags) {
  if (Array.isArray(rawTags)) {
    return rawTags.map(tag => String(tag).trim()).filter(Boolean);
  }
  if (!rawTags) {
    return [];
  }
  return String(rawTags)
    .split(/[,，]/)
    .map(tag => tag.trim())
    .filter(Boolean);
}

function extractTagValue(tags, prefixes) {
  for (const tag of tags) {
    const lowerTag = tag.toLowerCase();
    for (const prefix of prefixes) {
      const lowerPrefix = prefix.toLowerCase();
      if (lowerTag.startsWith(`${lowerPrefix}:`) || lowerTag.startsWith(`${lowerPrefix}=`)) {
        return tag.slice(lowerPrefix.length + 1).trim();
      }
    }
  }
  return '';
}

function resolveSplit(item, tags, options) {
  const splitById = buildSplitById(options.splits || {});
  if (splitById[item.id]) {
    return splitById[item.id];
  }
  const taggedSplit = extractTagValue(tags, ['split', 'domainrag:split']);
  if (SPLITS.includes(taggedSplit)) {
    return taggedSplit;
  }
  return '';
}

function buildSplitById(splits) {
  const splitById = {};
  for (const split of SPLITS) {
    const ids = Array.isArray(splits[split]) ? splits[split] : [];
    for (const id of ids) {
      splitById[String(id)] = split;
    }
  }
  return splitById;
}

function itemOverride(id, options) {
  const overrides = options.itemOverrides || options.item_overrides || {};
  return overrides[id] || {};
}

function resolveEnumValue(overrideValue, tagValue, defaultValue, allowed, fallback) {
  for (const value of [overrideValue, tagValue, defaultValue, fallback]) {
    const normalized = String(value || '').trim();
    if (allowed.has(normalized)) {
      return normalized;
    }
  }
  return fallback;
}

function resolveQualityScore(overrideValue, tagValue, defaultValue) {
  for (const value of [overrideValue, tagValue, defaultValue, DEFAULTS.quality_score]) {
    if (value === null || value === undefined || String(value).trim() === '') {
      continue;
    }
    const numberValue = Number(value);
    if (Number.isFinite(numberValue)) {
      return Math.max(0, Math.min(1, numberValue));
    }
  }
  return DEFAULTS.quality_score;
}

function assignFallbackSplits(prepared) {
  const splitCounts = countSplits(prepared);
  const missingSplits = SPLITS.filter(split => splitCounts[split] === 0);
  const unassigned = prepared.filter(entry => !entry.domainragItem.split);

  for (const split of missingSplits) {
    const entry = unassigned.shift();
    if (!entry) break;
    entry.domainragItem.split = split;
  }

  let index = 0;
  for (const entry of unassigned) {
    entry.domainragItem.split = SPLITS[index % SPLITS.length];
    index += 1;
  }
}

function validateBundle(prepared) {
  const errors = [];
  if (prepared.length === 0) {
    errors.push('no compatible DomainRAG items found');
    return errors;
  }

  const splitCounts = countSplits(prepared);
  for (const split of SPLITS) {
    if (splitCounts[split] === 0) {
      errors.push(`missing required split ${split}`);
    }
  }
  return errors;
}

function buildChunkRecords(prepared) {
  const chunks = [];
  const seen = new Set();
  for (const entry of prepared) {
    if (seen.has(entry.chunk.id)) {
      continue;
    }
    seen.add(entry.chunk.id);
    chunks.push({
      id: entry.chunk.id,
      name: entry.chunk.name,
      content: entry.chunk.content,
      metadata: entry.chunk.fileName ? { fileName: entry.chunk.fileName } : {}
    });
  }
  return chunks;
}

function buildStatistics(prepared) {
  return {
    chunk_count: buildChunkRecords(prepared).length,
    item_count: prepared.length,
    split_counts: countSplits(prepared)
  };
}

function countSplits(prepared) {
  const counts = { dev: 0, fresh_hard: 0, test: 0 };
  for (const entry of prepared) {
    const split = entry.domainragItem.split;
    if (Object.prototype.hasOwnProperty.call(counts, split)) {
      counts[split] += 1;
    }
  }
  return counts;
}

function parseMaybeJson(value) {
  if (typeof value !== 'string') {
    return value;
  }
  const trimmed = value.trim();
  if (!trimmed) {
    return '';
  }
  if (!['[', '{', '"'].includes(trimmed[0])) {
    return value;
  }
  try {
    return JSON.parse(trimmed);
  } catch {
    return value;
  }
}

function toArray(value) {
  if (Array.isArray(value)) {
    return value;
  }
  if (value === null || value === undefined || value === '') {
    return [];
  }
  return [value];
}

function toJsonl(records) {
  if (records.length === 0) {
    return '';
  }
  return `${records.map(record => JSON.stringify(record)).join('\n')}\n`;
}
