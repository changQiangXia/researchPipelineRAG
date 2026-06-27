import { NextResponse } from 'next/server';
import { db } from '@/lib/db/index';
import { buildEvalQuestionWhere } from '@/lib/db/evalDatasets';
import { buildDomainRAGBundle } from '@/lib/domainrag/exporter';

export const dynamic = 'force-dynamic';

const MAX_EXPORT_ROWS = 5000;

export async function GET(request, { params }) {
  try {
    const { projectId } = params;
    const total = await db.evalDatasets.count({
      where: { projectId, chunkId: { not: null } }
    });

    return NextResponse.json({
      route: 'domainrag-export',
      contract: ['chunks.jsonl', 'items.jsonl'],
      compatible_rows_with_chunk: total
    });
  } catch (error) {
    console.error('Failed to preview DomainRAG export:', error);
    return NextResponse.json(
      { error: error.message || 'DomainRAG export preview failed' },
      { status: 500 }
    );
  }
}

export async function POST(request, { params }) {
  try {
    const { projectId } = params;
    const body = await safeJson(request);
    const where = buildEvalQuestionWhere(projectId, {
      questionTypes: Array.isArray(body.questionTypes) ? body.questionTypes : undefined,
      tags: Array.isArray(body.tags) ? body.tags : undefined,
      keyword: body.keyword || undefined
    });
    where.chunkId = { not: null };

    const rows = await db.evalDatasets.findMany({
      where,
      include: {
        chunks: {
          select: {
            id: true,
            name: true,
            fileName: true,
            content: true
          }
        }
      },
      orderBy: { createAt: 'desc' },
      take: exportLimit(body.limit)
    });

    const bundle = buildDomainRAGBundle(rows, body);
    if (bundle.errors.length > 0) {
      return NextResponse.json(bundle, { status: 400 });
    }
    return NextResponse.json(bundle);
  } catch (error) {
    console.error('Failed to export DomainRAG bundle:', error);
    return NextResponse.json(
      { error: error.message || 'DomainRAG export failed' },
      { status: 500 }
    );
  }
}

async function safeJson(request) {
  try {
    return await request.json();
  } catch {
    return {};
  }
}

function exportLimit(limit) {
  const parsed = Number(limit);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    return MAX_EXPORT_ROWS;
  }
  return Math.min(parsed, MAX_EXPORT_ROWS);
}
